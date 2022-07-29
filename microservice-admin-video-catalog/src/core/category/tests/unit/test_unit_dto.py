
from dataclasses import asdict
from typing import Optional
import unittest

from datetime import datetime
from core.category.dto import CategoryOutput, CategoryOutputMapper
from core.category.entities import Category


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
            asdict(CategoryOutputMapper.to_output(category)),
            asdict(CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at.isoformat()
            ))
        )
