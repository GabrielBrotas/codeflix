#pylint: disable=unexpected-keyword-arg
from dataclasses import asdict
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch
from _shared.domain.exceptions import NotFoundException
from _shared.application.use_cases import UseCaseInterface
from category.application.dto import CategoryOutputMapper
from category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase
)
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemorySearchableRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):

    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemorySearchableRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemorySearchableRepository()
        self.use_case = CreateCategoryUseCase(category_repo=self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCaseInterface)

    def test_execute(self):
        # mock the insert function and keep the behavior, just to spy
        with patch.object(
            self.category_repo,
            'insert',
            wraps=self.category_repo.insert
        ) as spy_insert:
            input_params = CreateCategoryUseCase.Input(name="test")
            output = self.use_case.execute(input_params=input_params)

            spy_insert.assert_called_once()
            self.assertEqual(len(self.category_repo.find_all()), 1)

            expected_output = CreateCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name="test",
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at,
            )
            self.assertEqual(asdict(output), asdict(expected_output))


class TestGetCategoryUseCaseUnit(unittest.TestCase):

    use_case: GetCategoryUseCase
    category_repo: CategoryInMemorySearchableRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemorySearchableRepository()
        self.use_case = GetCategoryUseCase(category_repo=self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCaseInterface)

    def test_execute(self):
        category = Category(name="Movie")
        self.category_repo.items = [category]
        with patch.object(
            self.category_repo,
            'find_by_id',
            wraps=self.category_repo.find_by_id
        ) as spy_find_by_id:
            input_params = GetCategoryUseCase.Input(id=category.id)
            result = self.use_case.execute(input_params=input_params)

            spy_find_by_id.assert_called_once()

            expected_output = GetCategoryUseCase.Output(
                id=category.id,
                created_at=category.created_at,
                description=category.description,
                is_active=category.is_active,
                name=category.name,
            )

            self.assertEqual(asdict(result), asdict(expected_output))

    def test_execute_error(self):
        with self.assertRaises(NotFoundException) as assert_error:
            input_params = GetCategoryUseCase.Input(id="fake_id")
            self.use_case.execute(input_params=input_params)

        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID = fake_id"
        )


class TestListCategoriesUseCaseUnit(unittest.TestCase):

    use_case: GetCategoryUseCase
    category_repo: CategoryInMemorySearchableRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemorySearchableRepository()
        self.use_case = ListCategoriesUseCase(category_repo=self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCaseInterface)

    def test_execute_with_default_params(self):
        """
            return the category items in desc order by create_at
        """
        self.category_repo.items = [
            Category(name="Test 1"),
            Category(name="Test 2", created_at=datetime.now() +
                     timedelta(seconds=100))
        ]
        with patch.object(
            self.category_repo,
            'search',
            wraps=self.category_repo.search
        ) as spy_search:
            input_params = ListCategoriesUseCase.Input()
            output = self.use_case.execute(input_params=input_params)

            spy_search.assert_called_once()

            self.assertEqual(asdict(output), asdict(ListCategoriesUseCase.Output(
                items=list(
                    map(
                        CategoryOutputMapper.to_output,
                        self.category_repo.items[::-1]  # invert order
                    )
                ),
                current_page=1,
                last_page=1,
                per_page=15,
                total=2
            )))

    def test_execute_with_params(self):
        items = [
            Category(name="a"),
            Category(name="AAA"),
            Category(name="zxcAaa"),
            Category(name="c"),
            Category(name="DD")
        ]

        self.category_repo.items = items

        input_params = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort="name",
            sort_order="asc",
            filter="a"
        )

        output = self.use_case.execute(input_params=input_params)

        self.assertEqual(asdict(output), asdict(ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.to_output,
                    [items[1], items[0]]
                )
            ),
            current_page=1,
            last_page=2,
            per_page=2,
            total=3
        )))
