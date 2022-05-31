# sourcery skip: avoid-builtin-shadow
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from _shared.domain.entities import Entity

#? dataclass will help to maitain the class
#we just have to say the parameters we want and it will automatically create a constructor for us
#dataclass implements init, representation, equal, ...
#
#? kw_only will allow optional values in any order
#but by activating it we must specify the fields when create an instance, ex: Category(name="",...)

@dataclass(kw_only=True, frozen=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    #pylint: disable=unnecessary-lambda
    created_at: Optional[datetime] = field(  # it will just execute at the creation time
        default_factory=lambda: datetime.now()
    )

# print(vars(Category(name="Movie")))


# the constructor represents the creation of a category
# when we save on a database it represents the persistence of this data

#    ? Object Value
#    On programming we have some types like str, Object, int,...
#    but when we are talking about domain we need more semantics types
#
#    entity = set of attributes + entities + object value
#
#    ex: colored pencil
#    a child is drawing on a paper with a blue colored pencil
#    and suddenly this pencil breaks, the child can take a blue
#    pencil from another brand as long as it is the same color.
#
#    that's the concept of a object value, doesn't have and id, it has properties
#    the pencil dosen't has a identification, what matters for us is the color.
#
#    ex: Address
#
#    an object value must be immutable and equal to another OV if has the same values
