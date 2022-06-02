
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from .value_objects import UniqueEntityId
from .entities import Entity

# the generic can be anything but must inherit the Entity Type
GenericEntity = TypeVar('GenericEntity', bound=Entity)

class RepositoryInterface(Generic[GenericEntity], ABC):

    @abstractmethod
    def insert(self, entity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[GenericEntity]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id) -> None:
        raise NotImplementedError()
    