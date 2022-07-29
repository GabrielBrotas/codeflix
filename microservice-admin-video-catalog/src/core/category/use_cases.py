# pylint: disable=unexpected-keyword-arg
from dataclasses import asdict, dataclass
from typing import Optional
from core._shared.use_cases import UseCaseInterface
from core._shared.dto import (
    PaginationOutputMapper,
    SearchInput,
    PaginationOutput
)
from .repositories import CategoryRepositoryInterface
from .entities import Category
from .dto import CategoryOutput, CategoryOutputMapper


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(UseCaseInterface):
    category_repo: CategoryRepositoryInterface

    def execute(self, input_params: 'Input') -> 'Output':
        category = Category(
            name=input_params.name,
            description=input_params.description,
            is_active=input_params.is_active
        )
        self.category_repo.insert(category)
        return CategoryOutputMapper.to_output(category)

    # DTO
    @dataclass(slots=True, frozen=True)
    class Input:
        def __post_init__(self):
            if not self.is_active:
                object.__setattr__(self, 'is_active', Category.get_field('is_active').default)

        name: str
        # get the default values from the entity because it can change
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCaseInterface):
    category_repo: CategoryRepositoryInterface

    def execute(self, input_params: 'Input') -> 'Output':
        category = self.category_repo.find_by_id(
            entity_id=input_params.id
        )
        return CategoryOutputMapper.to_output(category)

    # DTO
    @dataclass(slots=True, frozen=True)
    class Input:
        # pylint: disable=invalid-name
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoriesUseCase(UseCaseInterface):
    category_repo: CategoryRepositoryInterface

    def execute(self, input_params: 'Input') -> 'Output':
        search_params = self.category_repo.SearchParams(**asdict(input_params))
        result = self.category_repo.search(
            search_params=search_params
        )
        return self.__to_output(result)

    def __to_output(self, result: CategoryRepositoryInterface.SearchResult):
        items = list(
            map(CategoryOutputMapper.to_output, result.items)
        )
        return PaginationOutputMapper.to_output(items, result)

    # DTO
    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass
        # page: Optional[int] = SearchParams.get_field('page').default NOSONAR
        # per_page: Optional[int] = SearchParams.get_field('per_page').default
        # sort: Optional[str] = SearchParams.get_field('sort').default
        # sort_order: Optional[str] = SearchParams.get_field('sort_order').default
        # filter: Optional[str]= SearchParams.get_field('filter').default

    @dataclass(slots=True, frozen=True)
    class Output(PaginationOutput[CategoryOutput]):
        pass


@dataclass(slots=True, frozen=True)
class DeleteCategoryUseCase(UseCaseInterface):
    category_repo: CategoryRepositoryInterface

    def execute(self, input_params: 'Input') -> 'Output':
        self.category_repo.delete(entity_id=input_params.id)
        return True

    @dataclass(slots=True, frozen=True)
    class Input:
        # pylint: disable=invalid-name
        id: str

    @dataclass(slots=True, frozen=True)
    class Output:
        pass
