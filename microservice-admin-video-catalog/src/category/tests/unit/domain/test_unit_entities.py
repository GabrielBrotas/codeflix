from datetime import date, datetime
from src.category.domain.entities import Category
from dataclasses import is_dataclass
import unittest  # another option = pytest;

class TestCategoryUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        default_category = Category(name="Movie")
        
        self.assertEqual(default_category.name, "Movie")
        self.assertEqual(default_category.description, None)
        self.assertEqual(default_category.is_active, True)
        self.assertIsInstance(default_category.created_at, datetime)

        created_at = datetime.now()
        category_with_props = Category(
            name="Movie", 
            description="Some description", 
            is_active= True, 
            created_at=created_at
        )

        self.assertEqual(category_with_props.name, "Movie")
        self.assertEqual(category_with_props.description, "Some description")
        self.assertEqual(category_with_props.is_active, True)
        self.assertEqual(category_with_props.created_at, created_at)
        self.assertIsInstance(category_with_props.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self):   
        category1 = Category(name="Movie")
        category2 = Category(name="Movie")

        self.assertNotEqual(category1, category2)
        self.assertNotEqual(
            category1.created_at.timestamp(), 
            category2.created_at.timestamp()
        )
