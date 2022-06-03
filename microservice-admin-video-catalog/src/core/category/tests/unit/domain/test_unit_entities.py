# pylint: disable=unexpected-keyword-arg
from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass
import unittest
from unittest.mock import patch  # another option = pytest;
from core.category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):  # sourcery skip: extract-duplicate-method
        # mock the validate method because we don`t want to test that function
        with patch.object(Category, 'validate') as mock_validate_method:
            default_category = Category(name="Movie")
            mock_validate_method.assert_called_once()
            self.assertEqual(default_category.name, "Movie")
            self.assertEqual(default_category.description, None)
            self.assertEqual(default_category.is_active, True)
            self.assertIsInstance(default_category.created_at, datetime)

            created_at = datetime.now()
            category_with_props = Category(
                name="Movie",
                description="Some description",
                is_active=True,
                created_at=created_at
            )

            self.assertEqual(category_with_props.name, "Movie")
            self.assertEqual(category_with_props.description,
                             "Some description")
            self.assertEqual(category_with_props.is_active, True)
            self.assertEqual(category_with_props.created_at, created_at)
            self.assertIsInstance(category_with_props.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self):
        with patch.object(Category, 'validate') as mock_validate_method:
            category1 = Category(name="Movie")
            mock_validate_method.assert_called_once()

            category2 = Category(name="Movie")

            self.assertNotEqual(category1, category2)
            self.assertNotEqual(
                category1.created_at.timestamp(),
                category2.created_at.timestamp()
            )

    def test_if_is_immutable(self):
        with patch.object(Category, 'validate'):
            with self.assertRaises(FrozenInstanceError):
                category = Category(name="Movie")
                category.name = "Movie Updated"

    def test_if_can_update_name_and_description(self):
        with patch.object(Category, 'validate'):
            category = Category(name="Movie")

            category.update("Movie1", "Description")

            self.assertEqual(category.name, "Movie1")
            self.assertEqual(category.description, "Description")

    def test_is_can_activate_and_deactivate_category(self):
        with patch.object(Category, 'validate'):
            category = Category(name="Movie")

            self.assertEqual(category.is_active, True)

            category.deactivate()
            self.assertEqual(category.is_active, False)

            category.activate()
            self.assertEqual(category.is_active, True)
