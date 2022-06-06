# pylint: disable=unexpected-keyword-arg,protected-access
import unittest
from datetime import datetime, timedelta
from core.category.entities import Category
from infraestructure.category.repository import CategoryInMemorySearchableRepository


class TestCategoryInMemoryRepositoryUnit(unittest.TestCase):

    repo: CategoryInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = CategoryInMemorySearchableRepository()

    def test_filter_params_null(self):
        entity = Category(name="Movie")
        items = [entity]

        items_filtered = self.repo._apply_filter(items, None)
        self.assertEqual(items_filtered, items)

    def test_filter(self):
        items = [
            Category(name="test"),
            Category(name="xpto"),
            Category(name="TeST")
        ]
        items_filtered = self.repo._apply_filter(items, "tes")
        self.assertEqual(items_filtered, [items[0], items[2]])

    def test_sort_by_created_at(self):
        items = [
            Category(name="test", created_at=datetime.now()),
            Category(name="xpto", created_at=datetime.now() +
                     timedelta(seconds=500)),
            Category(name="TeST", created_at=datetime.now() +
                     timedelta(seconds=300))
        ]
        items_sorted = self.repo._apply_sort(items, "created_at", "desc")
        print(items_sorted)
        self.assertEqual(items_sorted, [items[1], items[2], items[0]])
