"""
The standard library has a core module called "itertools", hence the "x" in this
module of eXtended iteration functions.
"""
from typing import Any, TypeVar, Optional, Callable, Iterable

T = TypeVar("T")
OneArgPredicate = Callable[[T], bool]


def first(pred: OneArgPredicate[T], iterable: Iterable, *, default: Optional[T] = None) -> Optional[T]:
    try:
        return next(filter(pred, iterable))
    except StopIteration:
        return default


def first_index(pred: OneArgPredicate[T], iterable: Iterable) -> int:
    # It's using the `first` function to find the first element of `iterable` that satisfies the predicate `pred`.
    idx_and_result = first(lambda i_r: pred(i_r[1]), enumerate(iterable))
    if idx_and_result is None:
        return -1

    return idx_and_result[0]
