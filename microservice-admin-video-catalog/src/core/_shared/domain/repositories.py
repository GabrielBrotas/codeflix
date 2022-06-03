
from abc import ABC, abstractmethod
from dataclasses import Field, dataclass, field
import math
from typing import Any, Generic, List, Optional, TypeVar
from .value_objects import UniqueEntityId
from .entities import Entity
from .exceptions import NotFoundException

# the generic can be anything but must inherit the Entity Type
GenericEntity = TypeVar('GenericEntity', bound=Entity)


class RepositoryInterface(Generic[GenericEntity], ABC):

    @abstractmethod
    def insert(self, entity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[GenericEntity]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id) -> None:
        raise NotImplementedError()


Input = TypeVar('Input')
Output = TypeVar('Output')


class SearchableRepositoryInterface(
    Generic[GenericEntity, Input, Output],
    RepositoryInterface[GenericEntity],
    ABC
):
    sortable_fields: List[str] = []

    @abstractmethod
    def search(self, search_params: Input) -> Output:
        raise NotImplementedError()


GenericFilter = TypeVar("GenericFilter", str, Any)


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[GenericFilter]):
    page: Optional[int] = 1
    per_page: Optional[int] = 15
    sort: Optional[str] = None
    sort_order: Optional[str] = None
    filter: Optional[GenericFilter] = None

    def __post_init__(self):
        self._normalize_page()
        self._normalize_per_page()
        self._normalize_sort()
        self._normalize_sort_order()
        self._normalize_filter()

    def _normalize_page(self):
        page = self._convert_to_int(self.page)
        if page <= 0:
            page = self._get_dataclass_default_value('page').default
        self.page = page

    def _normalize_per_page(self):
        per_page = self._convert_to_int(self.per_page)
        if per_page < 1:
            per_page = self._get_dataclass_default_value('per_page').default
        self.per_page = per_page

    def _normalize_sort(self):
        self.sort = None if self.sort == "" or self.sort is None or not str(self.sort).strip() \
            else str(self.sort)

    def _normalize_sort_order(self):
        if not self.sort:
            self.sort_order = None
            return

        sort_order = str(self.sort_order).lower().strip()
        self.sort_order = 'asc' if sort_order not in [
            "asc", "desc"] else sort_order

    def _normalize_filter(self):
        self.filter = None if self.filter == "" \
            or self.filter is None or not str(self.filter).strip() \
            else str(self.filter)

    def _convert_to_int(self, value: Any, default=0) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _get_dataclass_default_value(self, field_name):
        #pylint: disable=no-member
        return SearchParams.__dataclass_fields__[field_name]

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        # pylint: disable=no-member
        return cls.__dataclass_fields__[entity_field]


@dataclass(slots=True, kw_only=True, frozen=True)
class SearchResult(Generic[GenericEntity, GenericFilter]):
    items: List[GenericEntity]
    total: int
    current_page: int
    per_page: int
    last_page: int = field(init=False)  # not available on constructor
    sort: Optional[str] = None
    sort_order: Optional[str] = None
    filter: Optional[GenericFilter] = None

    def __post_init__(self):
        object.__setattr__(self, 'last_page', math.ceil(
            self.total / self.per_page))

    def to_dict(self):
        return {
            'items': self.items,
            'total': self.total,
            'current_page': self.current_page,
            'per_page': self.per_page,
            'last_page': self.last_page,
            'sort': self.sort,
            'sort_order': self.sort_order,
            'filter': self.filter
        }


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[GenericEntity], ABC):
    items: List[GenericEntity] = field(
        default_factory=lambda: []
    )

    def insert(self, entity) -> None:
        self.items.append(entity)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
        id_str = str(entity_id)
        return self._get(id_str)

    def find_all(self) -> List[GenericEntity]:
        return self.items

    def update(self, entity) -> None:
        entity_found = self._get(entity.id)
        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity_id) -> None:
        entity_found = self._get(entity_id)
        self.items.remove(entity_found)

    def _get(self, entity_id: str) -> GenericEntity:
        entity = next(filter(lambda item: item.id ==
                      entity_id, self.items), None)

        if not entity:
            raise NotFoundException(f'Entity not found using ID = {entity_id}')
        return entity


class InMemorySearchableRepository(
    Generic[GenericEntity, GenericFilter],
    InMemoryRepository[GenericEntity],
    SearchableRepositoryInterface[
        GenericEntity,
        SearchParams[GenericFilter],
        SearchResult[GenericEntity, GenericFilter]
    ],
    ABC
):

    def search(
        self,
        search_params: SearchParams[GenericFilter]
    ) -> SearchResult[GenericEntity, GenericFilter]:
        # filter
        filtered_items = self._apply_filter(self.items, search_params.filter)

        # order
        ordered_items = self._apply_sort(
            filtered_items, search_params.sort, search_params.sort_order)

        # pagination
        paginated_items = self._apply_paginate(
            ordered_items, search_params.page, search_params.per_page)

        return SearchResult(
            items=paginated_items,
            total=len(filtered_items),
            current_page=search_params.page,
            per_page=search_params.per_page,
            sort=search_params.sort,
            sort_order=search_params.sort_order,
            filter=search_params.filter
        )

    @abstractmethod
    def _apply_filter(
        self,
        items: List[GenericEntity],
        filter_param: GenericFilter | None
    ) -> List[GenericEntity]:
        raise NotImplementedError()

    def _apply_sort(
        self,
        items: List[GenericEntity],
        sort: str | None,
        sort_order: str | None
    ) -> List[GenericEntity]:
        if sort and sort in self.sortable_fields:
            is_reverse = sort_order == 'desc'
            return sorted(items, key=lambda item: getattr(item, sort), reverse=is_reverse)

        return items

    def _apply_paginate(
        self,
        items: List[GenericEntity],
        page: int,
        per_page: int
    ) -> List[GenericEntity]:
        offset = (page - 1) * per_page
        limit = offset + per_page
        return items[slice(offset, limit)]
