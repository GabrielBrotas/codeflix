from dataclasses import dataclass, field
from typing import Dict, List, TypeVar


ErrorFields = Dict[str, List[str]]  # type, {string: [list]}
PropsValidated = TypeVar('PropsValidated')  # can be anything

# Notification Pattern,


@dataclass()
class Notification:
    errors: ErrorFields = field(  # it will just execute at the creation time
        default_factory=lambda: {}
    )

    def add_error(self, key: str, msg: str) -> None:
        if key not in self.errors:
            self.errors[key] = []

        self.errors[key].append(msg)

    def has_errors(self) -> bool:
        return any(len(self.errors[key]) > 0 for key in self.errors)

    def get_errors(self) -> 'ErrorFields':
        return self.errors

    def get_errors_msg(self) -> str:
        error_msg = ''
        for key in self.errors:
            if len(self.errors[key]) > 0:
                error_msg += f'{key}:'
                error_msg += ','.join(self.errors[key])
                error_msg += ';'

        return error_msg
