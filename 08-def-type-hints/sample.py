from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar("T")


def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError("size must be >= 1")
    result = list(population)
    shuffle(result)
    return result[:size]


"""
如果通过tuple[int, ...]调用，它与Sequence[int]相容，那么类型参数就是int，返回类型是list[int]
如果通过str调用，它与Sequence[str]相容，那么类型参数是str，返回类型是list[str]
"""
