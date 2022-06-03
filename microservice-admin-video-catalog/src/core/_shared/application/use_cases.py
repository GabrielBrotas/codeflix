
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputGeneric = TypeVar('InputGeneric')
OutputGeneric = TypeVar('OutputGeneric')


class UseCaseInterface(Generic[InputGeneric, OutputGeneric], ABC):

    @abstractmethod
    def execute(self, input_params: InputGeneric) -> OutputGeneric:
        raise NotImplementedError()
