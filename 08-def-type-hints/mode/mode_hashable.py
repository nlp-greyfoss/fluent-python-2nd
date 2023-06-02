from collections import Counter
from collections.abc import Iterable, Hashable
from typing import TypeVar

# 通过bound参数，为接收的类型设定了一个上限
HashableT = TypeVar("HashableT", bound=Hashable)


def mode(data: Iterable[HashableT]) -> HashableT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]


"""
Counter基于dict，它要求元素类型是hashable，所以引入Hashable似乎可以解决这个问题。
但Hashable作为返回类型就，意味着它只有__hash__方法，类型检查器不会允许我们对它的返回类型调用其他方法。

好的做法是，通过bound参数，为接收的类型设定了一个上限。
"""
