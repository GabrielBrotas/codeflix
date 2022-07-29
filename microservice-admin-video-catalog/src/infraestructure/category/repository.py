from typing import List
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from core._shared.value_objects import UniqueEntityId
from core.category.entities import Category
from core.category.repositories import CategoryRepositoryInterface
from core._shared.repositories import InMemorySearchableRepository
from core._shared.exceptions import NotFoundException
from infraestructure.db import SessionLocal
from .schema import CategorySchema

class CategoryRepository(CategoryRepositoryInterface):

    def insert(self, entity: Category) -> None:
        with SessionLocal() as session:
            print(entity)
            category = CategorySchema(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                is_active=entity.is_active,
                # created_at=entity.created_at
            )
            print(category)
            session.add(category)
            session.commit()

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Category:
        with SessionLocal() as session:
            id_str = str(entity_id)
            return self._get(id_str, session)

    def find_all(self) -> List[Category]:
        with SessionLocal() as session:
            categories = session.query(CategorySchema).all()
            return categories

    def update(self, entity) -> None:
        with SessionLocal() as session:
            entity_found = self._get(entity.id, session)
            # index = self.items.index(entity_found)
            # self.items[index] = entity
            return None

    def delete(self, entity_id) -> None:
        with SessionLocal() as session:
            entity_found = self._get(entity_id, session)
            session.delete(entity_found)
            session.commit()

    def _get(self, entity_id: str, session) -> Category:
        entity = session.execute(
            select(Category).filter_by(id=entity_id).first()
            )
        if not entity:
            raise NotFoundException(f'Entity not found using ID = {entity_id}')
        return entity

    def search(
        self,
        search_params: CategoryRepositoryInterface.SearchParams
    ) -> CategoryRepositoryInterface.SearchResult:
        with SessionLocal() as session:
            is_reverse_order = search_params.sort_order == 'desc'

            # filter items, order and paginate
            items = session.query(CategorySchema).all()
        return CategoryRepositoryInterface.SearchResult(
            items=items,
            total=len(items),
            current_page=search_params.page,
            per_page=search_params.per_page,
            sort=search_params.sort,
            sort_order=search_params.sort_order,
            filter=search_params.filter
        )
    

class CategoryInMemorySearchableRepository(
    CategoryRepositoryInterface,
    InMemorySearchableRepository
):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(
        self, 
        items: List[Category],
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
