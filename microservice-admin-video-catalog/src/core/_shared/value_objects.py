# sourcery skip: avoid-builtin-shadow
from abc import ABC
from dataclasses import dataclass, field, fields
import json
import uuid
from .exceptions import InvalidUUIDException

# ABC - Abstract Base Class


@dataclass(frozen=True, slots=True)
class ValueObject(ABC):
    def __str__(self) -> str:
        fields_name = [field.name for field in fields(self)]

        return str(getattr(self, fields_name[0])) \
            if len(fields_name) == 1 \
            else json.dumps({field_name: getattr(self, field_name) for field_name in fields_name})

# Frozen will not allow update an attribute once the VO is created
# We need this because according to DDD an VO must be immutable


@dataclass(frozen=True, slots=True)
class UniqueEntityId(ValueObject):

    id: str = field( # pylint: disable=invalid-name
        default_factory= uuid.uuid4
    )

    # it will be called after the constructor
    def __post_init__(self):
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', id_value)
        self.__validate()

    # python way to specify a private method
    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUUIDException() from ex
