
from typing import Optional
import unittest

from datetime import datetime
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category


class TestDtoUnit(unittest.TestCase):

    def test_category_dto(self):
        self.assertEqual(CategoryOutput.__annotations__, {
            'created_at': datetime,
            'description': Optional[str],
            'id': str,
            'is_active': bool,
            'name': str
        })

    def test_category_output_mapper(self):
        # pylint: disable=unexpected-keyword-arg
        category = Category(name="Movie")

        self.assertEqual(
            CategoryOutputMapper.to_output(category),
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at
            )
        )
