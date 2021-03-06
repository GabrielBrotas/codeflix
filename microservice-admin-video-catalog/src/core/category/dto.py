
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from core.category.entities import Category


@dataclass(frozen=True, slots=True)
class CategoryOutput:
    # pylint: disable=invalid-name
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CategoryOutputMapper:
    @staticmethod
    def to_output(category: Category) -> CategoryOutput:
        return CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at.isoformat() if category.created_at else None
        )
