from abc import ABC
from dataclasses import dataclass, field, asdict
from _shared.domain.value_objects import UniqueEntityId


@dataclass(frozen=True)
class Entity(ABC):

    # pylint: disable=unnecessary-lambda
    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId()
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
