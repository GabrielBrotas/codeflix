
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from _shared.domain.repositories import SearchResult

GenericFilter = TypeVar('GenericFilter')
GenericItem = TypeVar('GenericItem')


@dataclass(frozen=True, slots=True)
class SearchInput(Generic[GenericFilter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_order: Optional[str] = None
    filter: Optional[GenericFilter] = None


@dataclass(frozen=True, slots=True)
class PaginationOutput(Generic[GenericItem]):
    items: List[GenericItem]
    total: int
    current_page: int
    per_page: int
    last_page: int


class PaginationOutputMapper:
    @staticmethod
    def to_output(items: List[GenericItem], result: SearchResult) -> PaginationOutput[GenericItem]:
        return PaginationOutput(
            items=items,
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page,
        )
