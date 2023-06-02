from collections import Counter
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def mode(data: Iterable[T]) -> T:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]


"""
但是这种写法又有问题，因为可能有些类型不能hash，即不能作为Counter的参数
"""
