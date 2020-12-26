from dataclasses import field, Field, dataclass
from enum import Enum
from typing import TypeVar, Type

T = TypeVar('T')


def empty_list():
    return field(default_factory=lambda: [])


def empty_dict():
    return field(default_factory=lambda: {})


def empty_class(clazz: Type[T]):
    return field(default_factory=clazz)


class RGender(Enum):
    male = 'male'
    female = 'female'
    neutral = 'neutral'
    both = 'both'
    other = 'other'
    invalid = 'invalid'

@dataclass
class RValue:
    value: int
    unit: str
