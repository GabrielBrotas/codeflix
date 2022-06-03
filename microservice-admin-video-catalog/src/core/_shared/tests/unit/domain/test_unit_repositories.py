# pylint: disable=unexpected-keyword-arg,protected-access
from dataclasses import dataclass
from typing import List, Optional
import unittest
from _shared.domain.exceptions import NotFoundException
from _shared.domain.repositories import (
    GenericEntity,
    GenericFilter,
    InMemoryRepository,
    InMemorySearchableRepository,
    RepositoryInterface,
    SearchParams,
    SearchResult,
    SearchableRepositoryInterface
)
from _shared.domain.entities import Entity


class TestRepositoryInterfaceUnit(unittest.TestCase):

    def test_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()  # pylint: disable=abstract-class-instantiated

        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface" +
            " with abstract methods delete, find_all, find_by_id, insert, update"
        )


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):

    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_insert(self):
        self.assertEqual(self.repo.find_all(), [])

        entity = StubEntity(name="test", price=10)
        self.repo.insert(entity)
        self.assertEqual(self.repo.find_all(), [entity])

    def test_find_by_id(self):
        entity = StubEntity(name="test", price=10)
        self.repo.insert(entity)
        self.assertEqual(self.repo.find_by_id(entity.id), entity)

        with self.assertRaises(NotFoundException) as assert_error:
            self.assertEqual(self.repo.find_by_id("123"), entity)

        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID = 123"
        )

    def test_delete(self):
        entity = StubEntity(name="test 2", price=10)
        self.repo.insert(entity)
        self.repo.delete(entity.id)

        with self.assertRaises(NotFoundException) as assert_error:
            self.assertEqual(self.repo.find_by_id(entity.id), entity)

        self.assertEqual(
            assert_error.exception.args[0],
            f'Entity not found using ID = {entity.id}'
        )

    def test_update(self):
        entity = StubEntity(name="test 4", price=10)
        self.repo.insert(entity)

        object.__setattr__(entity, "name", "test 5")
        self.repo.update(entity)

        self.assertEqual(
            self.repo.find_by_id(entity.id).name,
            "test 5"
        )


class TestSearchableRepositoryInterfaceUnit(unittest.TestCase):

    def test_throw_error_if_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            SearchableRepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class SearchableRepositoryInterface with " +
            "abstract methods delete, find_all, find_by_id, insert, search, update"
        )


class TestSearchParamsUnit(unittest.TestCase):

    def test_props_annotation(self):
        self.assertEqual(SearchParams.__annotations__, {
            'page': Optional[int],
            'per_page': Optional[int],
            'sort': Optional[str],
            'sort_order': Optional[str],
            'filter': Optional[GenericFilter]
        })

    def test_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': "", 'expected': 1},
            {'page': "  ", 'expected': 1},
            {'page': "asda", 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': "0", 'expected': 1},
            {'page': "-1", 'expected': 1},
            {'page': "-10", 'expected': 1},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': [], 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 5.5, 'expected': 5},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
            {'page': 3, 'expected': 3},
        ]

        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['expected'])

    def test_per_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': "", 'expected': 15},
            {'per_page': "  ", 'expected': 15},
            {'per_page': "asda", 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': "0", 'expected': 15},
            {'per_page': "-10", 'expected': 15},
            {'per_page': "-1", 'expected': 15},
            # True is converted to 1 and False to 0
            {'per_page': True, 'expected': 1},
            {'per_page': False, 'expected': 15},
            {'per_page': [], 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 5.5, 'expected': 5},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
            {'per_page': 3, 'expected': 3},
        ]

        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'])

    def test_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': "", 'expected': None},
            {'sort': "  ", 'expected': None},
            {'sort': "fake", 'expected': "fake"},
            {'sort': 0, 'expected': '0'},
            {'sort': -1, 'expected': '-1'},
            {'sort': "0", 'expected': '0'},
            {'sort': "-10", 'expected': '-10'},
            {'sort': True, 'expected': 'True'},
            {'sort': False, 'expected': 'False'},
            {'sort': [], 'expected': '[]'},
            {'sort': {}, 'expected': '{}'},
            {'sort': 5.5, 'expected': '5.5'},
        ]

        for i in arrange:
            params = SearchParams(sort=i['sort'])
            self.assertEqual(params.sort, i['expected'])

    def test_sort_order_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_order)

        arrange = [
            {'sort_order': None, 'expected': 'asc'},
            {'sort_order': "", 'expected': 'asc'},
            {'sort_order': "  ", 'expected': 'asc'},
            {'sort_order': "fake", 'expected': 'asc'},
            {'sort_order': 0, 'expected': 'asc'},
            {'sort_order': -1, 'expected': 'asc'},
            {'sort_order': "0", 'expected': 'asc'},
            {'sort_order': "-10", 'expected': 'asc'},
            {'sort_order': True, 'expected': 'asc'},
            {'sort_order': False, 'expected': 'asc'},
            {'sort_order': [], 'expected': 'asc'},
            {'sort_order': {}, 'expected': 'asc'},
            {'sort_order': "aSc", 'expected': 'asc'},
            {'sort_order': "desc", 'expected': 'desc'},
            {'sort_order': "DeSc", 'expected': 'desc'},
        ]

        for i in arrange:
            params = SearchParams(sort="Name", sort_order=i['sort_order'])
            self.assertEqual(params.sort_order, i['expected'])

    def test_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filter)

        arrange = [
            {'filter': None, 'expected': None},
            {'filter': "", 'expected': None},
            {'filter': "  ", 'expected': None},
            {'filter': "fake", 'expected': "fake"},
            {'filter': 0, 'expected': '0'},
            {'filter': -1, 'expected': '-1'},
            {'filter': "0", 'expected': '0'},
            {'filter': "-10", 'expected': '-10'},
            {'filter': True, 'expected': 'True'},
            {'filter': False, 'expected': 'False'},
            {'filter': [], 'expected': '[]'},
            {'filter': {}, 'expected': '{}'},
            {'filter': 5.5, 'expected': '5.5'},
        ]

        for i in arrange:
            params = SearchParams(filter=i['filter'])
            self.assertEqual(params.filter, i['expected'])


class TestSearchResultUnit(unittest.TestCase):

    def test_props_annotation(self):
        self.assertEqual(SearchResult.__annotations__, {
            'items': List[GenericEntity],
            'total': int,
            'current_page': int,
            'per_page': int,
            'last_page': int,
            'sort': Optional[str],
            'sort_order': Optional[str],
            'filter': Optional[GenericFilter]
        })

    def test_constructor(self):
        entity = StubEntity(name="fake", price=10)
        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2
        )

        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': None,
            'sort_order': None,
            'filter': None
        })

        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2,
            sort="name",
            sort_order="desc",
            filter="test"
        )

        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': "name",
            'sort_order': "desc",
            'filter': 'test'
        })

    def test_last_page_attr(self):
        entity = StubEntity(name="fake", price=10)
        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=15
        )

        self.assertEqual(result.last_page, 1)

        result = SearchResult(
            items=[entity, entity],
            total=5,
            current_page=1,
            per_page=2
        )
        self.assertEqual(result.last_page, 3)


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    sortable_fields: List[str] = ["name"]

    def _apply_filter(
        self,
        items: List[GenericEntity],
        filter_param: GenericFilter | None
    ) -> List[GenericEntity]:
        if filter_param:
            filter_obj = filter(lambda item: filter_param.lower() in item.name.lower()
                                or filter_param == str(item.price), items)
            return list(filter_obj)
        return items


class TestInMemorySearchableRepositoryUnit(unittest.TestCase):

    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        entity1 = StubEntity(name="test", price=5)
        entity2 = StubEntity(name="fake", price=15)
        entity3 = StubEntity(name="tes", price=2)

        items = [entity1]

        result = self.repo._apply_filter(items, None)
        self.assertEqual(result, items)

        items = [entity1, entity2, entity3]
        result = self.repo._apply_filter(items, 'tes')
        self.assertEqual(result, [entity1, entity3])

        result = self.repo._apply_filter(items, '5')
        self.assertEqual(result, [entity1])

    def test__apply_sort(self):
        entity1 = StubEntity(name="a", price=5)
        entity2 = StubEntity(name="c", price=15)
        entity3 = StubEntity(name="b", price=2)

        items = [entity1, entity2, entity3]
        result = self.repo._apply_sort(items, None, None)
        self.assertEqual(result, items)

        result = self.repo._apply_sort(items, 'name', 'desc')
        self.assertEqual(result, [entity2, entity3, entity1])

        result = self.repo._apply_sort(items, 'name', 'asc')
        self.assertEqual(result, [entity1, entity3, entity2])

        result = self.repo._apply_sort(items, 'items', 'asc')
        self.assertEqual(result, items)

    def test__apply_paginate(self):
        entity1 = StubEntity(name="a", price=5)
        entity2 = StubEntity(name="b", price=15)
        entity3 = StubEntity(name="c", price=2)
        entity4 = StubEntity(name="d", price=2)

        items = [entity1, entity2, entity3, entity4]

        result = self.repo._apply_paginate(items, 1, 2)
        self.assertEqual(result, [entity1, entity2])

        result = self.repo._apply_paginate(items, 2, 2)
        self.assertEqual(result, [entity3, entity4])

        result = self.repo._apply_paginate(items, 3, 2)
        self.assertEqual(result, [])

    def test_search(self):
        entity1 = StubEntity(name="a", price=5)
        entity2 = StubEntity(name="b", price=15)
        entity3 = StubEntity(name="c", price=2)
        entity4 = StubEntity(name="d", price=2)
        entity5 = StubEntity(name="xx", price=2)

        self.repo.insert(entity1)
        self.repo.insert(entity2)
        self.repo.insert(entity3)
        self.repo.insert(entity4)
        self.repo.insert(entity5)

        search_params = SearchParams(
            page=1,
            per_page=3,
            sort="name",
            sort_order="desc",
            filter=None
        )

        result = self.repo.search(search_params=search_params)
        expected_result = SearchResult(
            items=[entity5, entity4, entity3],
            total=5,
            current_page=1,
            per_page=3,
            sort="name",
            sort_order="desc",
            filter=None
        )

        self.assertEqual(result, expected_result)
