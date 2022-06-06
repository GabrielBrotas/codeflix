#pylint: disable=unexpected-keyword-arg
import unittest
from core.category.entities import Category
from core._shared.exceptions import EntityValidationException


class TestCategoryIntegration(unittest.TestCase):

    def test_invalid_name_cases(self):
        invalid_datas = [
            {
                'name': None,
                'error_msg': 'name:The name is required;'  # NOSONAR
            },
            {
                'name': '',
                'error_msg': 'name:The name is required;'
            },
            {
                'name': 't'*256,
                'error_msg': 'name:The name length must be smaller than 255;'
            },
            {
                'name': 12,
                'error_msg': 'name:The name must be a string;'
            },
        ]
        for i in invalid_datas:
            with self.assertRaises(EntityValidationException) as assert_error:
                Category(name=i['name'])

            self.assertEqual(
                assert_error.exception.args[0], 'Entity Validation Error')  # NOSONAR
            self.assertEqual(assert_error.exception.error,
                             i['error_msg'])  # NOSONAR

    def test_invalid_description_cases(self):
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name='valid name', description=123)
        self.assertEqual(
            assert_error.exception.args[0],
            'Entity Validation Error'
        )
        self.assertEqual(
            assert_error.exception.error,
            'description:The description must be a string;'
        )

        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name='t'*255, description='d'*256)
        self.assertEqual(
            assert_error.exception.error,
            'description:The description length must be smaller than 255;'
        )

    def test_invalid_is_active_cases(self):
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name='valid name', is_active=5)
        self.assertEqual(assert_error.exception.error,
                         'is_active:The is_active must be boolean;')

    def test_invalid_composed_errors(self):
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name=None, description=1)
        self.assertEqual(
            assert_error.exception.error,
            'name:The name is required;description:The description must be a string;'
        )

        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name=None, description=None, is_active=123)
        self.assertEqual(
            assert_error.exception.error,
            'name:The name is required;is_active:The is_active must be boolean;'
        )

    def test_valid_cases(self):
        try:
            Category(name='Movie')
            Category(name='Movie', description=None)
            Category(name='Movie', description='')
            Category(name='Movie', is_active=False)
            Category(name='Movie', is_active=True)
        except EntityValidationException as exception:
            self.fail(f'Some prop is not valid. Error: {exception.error}')

    def test_update_cases(self):
        category = Category(name='Movie')
        with self.assertRaises(EntityValidationException) as assert_error:
            category.update('', '')

        self.assertEqual(assert_error.exception.error,
                         'name:The name is required;')

        with self.assertRaises(EntityValidationException) as assert_error:
            category.update(123, '')  # NOSONAR
        self.assertEqual(assert_error.exception.error,
                         'name:The name must be a string;')
