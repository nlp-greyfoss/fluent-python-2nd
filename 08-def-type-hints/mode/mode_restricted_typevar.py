from collections import Counter
from collections.abc import Iterable
from typing import TypeVar
from decimal import Decimal
from fractions import Fraction


NumberT = TypeVar("NumberT", float, Decimal, Fraction)


def mode(data: Iterable[NumberT]) -> NumberT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]


"""
这样就比mode_float和mode_typevar好多了。但如果要支持str的话，我们也许可以在TypeVar中加入str，但这个命名又有问题，而且这样对于扩展性不好。
"""
