import json
from typing import IO, Generic, TypeVar, Type, Iterable

from lib.data.convert import class_to_json, json_to_class

T = TypeVar('T')


class JSONReader(Generic[T]):
    def __init__(self, io: IO, clazz: Type[T]):
        self.io = io
        self.clazz = clazz

    def __iter__(self) -> Iterable[T]:
        for line in self.io.readlines():
            yield json_to_class(json.loads(line), self.clazz)


class JSONWriter(Generic[T]):
    def __init__(self, io: IO):
        self.io = io

    def write(self, data: T):
        json.dump(class_to_json(data), self.io, ensure_ascii=False)
        self.io.write('\n')
