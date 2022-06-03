from dataclasses import dataclass
from typing import Any, Optional
from _shared.domain.exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str
    throw_error: Optional[bool] = False
    error: Optional[str] = None

    @staticmethod
    def values(value: Any, prop: str, throw_error: bool = False):
        return ValidatorRules(value, prop, throw_error)

    def required(self) -> 'ValidatorRules':
        if self.has_error():
            return self

        if self.value is None or self.value == '':
            error_msg = f"The {self.prop} is required"
            if self.throw_error:
                raise ValidationException(error_msg)
            self._set('error', error_msg)
        return self

    def string(self) -> 'ValidatorRules':
        if self.has_error():
            return self

        if self.value is not None and not isinstance(self.value, str):
            error_msg = f"The {self.prop} must be a string"
            if self.throw_error:
                raise ValidationException(error_msg)
            self._set('error', error_msg)
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if self.has_error():
            return self

        if self.value is not None and len(self.value) > max_length:
            error_msg = f"The {self.prop} length must be smaller than {max_length}"
            if self.throw_error:
                raise ValidationException(error_msg)
            self._set('error', error_msg)
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.has_error():
            return self

        if self.value is not None and self.value is not True and self.value is not False:
            error_msg = f"The {self.prop} must be boolean"
            if self.throw_error:
                raise ValidationException(error_msg)
            self._set('error', error_msg)
        return self

    def has_error(self) -> bool:
        return self.error and len(self.error) > 0

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
