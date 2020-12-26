from enum import Enum, EnumMeta
from typing import TypeVar, Type, Any, Optional, Tuple, List, Collection

T = TypeVar('T')


def json_to_class(data: Any, root_class: Type[T]) -> T:
    return _to_class(data, root_class)


def class_to_json(data: T) -> Any:
    root_class: Type[T] = data.__class__
    return _to_json(data, root_class)


_collection_names = {
    'List': list,
    'Set': set,
    'Tuple': tuple,
    'Dict': dict
}


def _to_class(data, clazz):
    is_collection = _extract_collection(clazz)
    is_opt = _is_optional(clazz)
    if data is None:
        return None
    if is_opt is not None:
        if data is None:
            return None
        else:
            return _to_json(data, is_opt)
    elif is_collection is None:
        if isinstance(clazz, EnumMeta):
            return clazz(data) if data is not None else None
        elif not hasattr(clazz, '__annotations__'):
            return data
        else:
            return clazz(**{
                k: _to_class(data[k], t) if k in data else None
                for k, t in clazz.__annotations__.items()
            })
    else:
        c_type, args = is_collection
        if c_type is tuple:
            if len(args) == 2 and args[1] is Ellipsis:
                t = args[0]
                return tuple(
                    _to_class(d, t)
                    for d in data
                )
            else:
                return tuple(
                    _to_class(d, t)
                    for d, t in zip(data, args)
                )
        else:
            return c_type([
                _to_class(d, args[0])
                for d in data
            ])


def _to_json(data, clazz):
    is_collection = _extract_collection(clazz)
    is_opt = _is_optional(clazz)
    if data is None:
        return None
    if is_opt is not None:
        if data is None:
            return None
        else:
            return _to_json(data, is_opt)
    elif is_collection is None:
        if isinstance(clazz, EnumMeta) and data is not None:
            return data.value
        elif not hasattr(clazz, '__annotations__'):
            return data
        else:
            return {
                k: _to_json(getattr(data, k), t)
                for k, t in clazz.__annotations__.items()
            }
    else:
        c_type, args = is_collection
        if c_type is tuple:
            if len(args) == 2 and args[1] is Ellipsis:
                t = args[0]
                return [
                    _to_json(d, t)
                    for d in data
                ]
            else:
                return [
                    _to_json(d, t)
                    for d, t in zip(data, args)
                ]
        else:
            return [
                _to_json(d, args[0])
                for d in data
            ]


NoneType = type(None)


def _is_optional(d):
    if hasattr(d, '_name') and d._name == 'Union' and len(d.args) == 2 and d.args[1] == NoneType:
        return d.args[0]
    else:
        return None


def _extract_collection(d) -> Optional[Tuple[type, Tuple[type, ...]]]:
    if hasattr(d, '_name') and d._name is not None:
        tp = _collection_names[d._name]
        args = d.__args__
        return tp, args
    else:
        return None
