# sourcery skip: avoid-builtin-shadow
# pylint: disable=trailing-whitespace
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from _shared.domain.entities import Entity
from _shared.domain.exceptions import EntityValidationException, ValidationException
from _shared.domain.validators import ValidatorRules
from _shared.domain.notification import Notification

#? dataclass will help to maitain the class
#we just have to say the parameters we want and it will automatically create a constructor for us
#dataclass implements init, representation, equal, ...
#
#? kw_only will allow optional values in any order
#but by activating it we must specify the fields when create an instance, ex: Category(name="",...)

#? slots will help us with performance, that way we canno't assign another variable to this class
# ex: Catory().xpto = '123', because slots will disable the dynamic class
# but now we have a better performance because we know the exact struct we will have

@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    #pylint: disable=unnecessary-lambda
    created_at: Optional[datetime] = field(  # it will just execute at the creation time
        default_factory=lambda: datetime.now()
    )
    
    def __post_init__(self):
        if not self.created_at:
            self._set('created_at', datetime.now())
        self.validate()

    def update(self, name: str, description: str):
        self._set('name', name)
        self._set('description', description)
        self.validate()

    def activate(self):
        self._set('is_active', True)
    
    def deactivate(self):
        self._set('is_active', False)

    def validate(self):
        notification = Notification()
        name_validator = ValidatorRules(self.name, "name").required().string().max_length(255)
        desc_validator = ValidatorRules(self.description, "description").string().max_length(255)
        is_active_validator = ValidatorRules(self.is_active, "is_active").boolean()

        if name_validator.has_error():
            notification.add_error('name', name_validator.error)

        if desc_validator.has_error():
            notification.add_error('description', desc_validator.error)

        if is_active_validator.has_error():
            notification.add_error('is_active', is_active_validator.error)
        
        if notification.has_errors():
            raise EntityValidationException(notification.get_errors_msg())

# print(vars(Category(name="Movie")))
# the constructor represents the creation of a category
# when we save on a database it represents the persistence of this data
