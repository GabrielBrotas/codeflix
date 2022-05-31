# sourcery skip: avoid-builtin-shadow
from dataclasses import dataclass, field
from src._shared.domain.exceptions import InvalidUUIDException
import uuid

@dataclass()
class UniqueEntityId:

    id: str = field(
        default_factory=lambda: uuid.uuid4()
        )

    # it will be called after the constructor
    def __post_init__(self):
        self.id = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        self.__validate()

    # python way to specify a private method
    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUUIDException() from ex

# UniqueEntityId()
