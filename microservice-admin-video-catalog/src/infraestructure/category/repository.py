from typing import List
from core.category.entities import Category
from core.category.repositories import CategoryRepository
from core._shared.repositories import InMemorySearchableRepository


class CategoryInMemorySearchableRepository(
    CategoryRepository,
    InMemorySearchableRepository
):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(
        self, items: List[Category],
        filter_param: str = None
    ) -> List[Category]:
        if filter_param:
            filter_obj = filter(
                lambda item: filter_param.lower() in item.name.lower(),
                items
            )
            return list(filter_obj)
        return items

    def _apply_sort(
        self,
        items: List[Category],
        sort: str = None,
        sort_order: str = None
    ) -> List[Category]:
        return super()._apply_sort(items, sort, sort_order) \
            if sort \
            else super() ._apply_sort(items, "created_at", "desc") \

# class CategoryInMemoryRepository(CategoryRepository, InMemoryRepository): NOSONAR
#     def insert(self, entity) -> None:
#         self.items.append(entity)

#     def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
#         id_str = str(entity_id)
#         return self._get(id_str)

#     def find_all(self) -> List[GenericEntity]:
#         return self.items

#     def update(self, entity) -> None:
#         entity_found = self._get(entity.id)
#         index = self.items.index(entity_found)
#         self.items[index] = entity

#     def delete(self, entity_id) -> None:
#         entity_found = self._get(entity_id)
#         self.items.remove(entity_found)

#     def _get(self, entity_id: str) -> GenericEntity:
#         entity = next(filter(lambda item: item.id == entity_id, self.items), None)

#         if not entity:
#             raise NotFoundException(f'Entity not found using ID = {entity_id}')
#         return entity
