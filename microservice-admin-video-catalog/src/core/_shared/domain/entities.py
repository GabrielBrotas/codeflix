from abc import ABC
from dataclasses import Field, dataclass, field, asdict
from typing import Any
from core._shared.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class Entity(ABC):

    unique_entity_id: UniqueEntityId = field(
        default_factory=UniqueEntityId
    )

    # pylint: disable=invalid-name
    @property
    def id(self):
        return str(self.unique_entity_id)

    def to_dict(self):
        entity_dict = asdict(self)
        # remove the default unique_entity_id
        entity_dict.pop('unique_entity_id')
        entity_dict['id'] = self.id  # and add the id in the string format

        return entity_dict

    # make it easy to update an value
    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        # pylint: disable=no-member
        return cls.__dataclass_fields__[entity_field]
