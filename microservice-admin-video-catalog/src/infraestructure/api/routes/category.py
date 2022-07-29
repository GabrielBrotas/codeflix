from typing import Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel # pylint: disable=no-name-in-module
from core._shared.dto import SearchInput
from core.category.use_cases import CreateCategoryUseCase, ListCategoriesUseCase
from infraestructure.category.repository import CategoryRepository

categoryRouter = APIRouter(
    prefix='/categories',
    tags=["category"]
)

category_repo = CategoryRepository()

@categoryRouter.get("/")
async def list_categories():
    try:
        search_input = SearchInput()
        list_categories_use_case = ListCategoriesUseCase(category_repo)

        items = list_categories_use_case.execute(search_input)

        return {"success": True, "items": items}
    except Exception as error: # pylint: disable=broad-except
        print(error)
        return {"success": False, "error": "somethin went wrong"}

class CreateCategoryDTO(BaseModel):
    name: str
    description: Union[str, None]
    is_active: Optional[bool]

@categoryRouter.post("/")
async def create_categories(item: CreateCategoryDTO):
    try:
        cc_input = CreateCategoryUseCase.Input(
            name=item.name,
            description=item.description,
            is_active=item.is_active
        )

        create_category_use_case = CreateCategoryUseCase(category_repo)

        output = create_category_use_case.execute(input_params=cc_input)

        return {"success": True, "category": output}
    except Exception as error: # pylint: disable=broad-except
        print(error)
        return {"success": False, "error": "somethin went wrong"}
