from abc import ABC
from core._shared.repositories import (
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
    SearchableRepositoryInterface
)
from .entities import Category

# private class
class _SearchParams(DefaultSearchParams):
    pass

# private class
class _SearchResult(DefaultSearchResult):
    pass


class CategoryRepositoryInterface(
    SearchableRepositoryInterface[
        Category, _SearchParams, _SearchResult
    ],
    ABC
):
    SearchParams = _SearchParams
    SearchResult = _SearchResult

    # inner class, only available here
    # class SearchParams(DefaultSearchParams):
    #     pass

    # inner class, only available here
    # class SearchResult(DefaultSearchResult):
    #     pass
