from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .notification import ErrorFields

class InvalidUUIDException(Exception):

    # pylint: disable=useless-super-delegation
    def __init__(self, error='ID must be a valid UUID') -> None:
        super().__init__(error)

class ValidationException(Exception):
    pass

class EntityValidationException(Exception):
    error: 'ErrorFields'
    def __init__(self, error: 'ErrorFields') -> None:
        self.error = error
        super().__init__("Entity Validation Error")
