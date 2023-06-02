from collections import Counter
from collections.abc import Iterable


def mode(data: Iterable[float]) -> float:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]


"""
这种写法比较受限，只能用于int或float类型，但Python还有其他数字类型。
"""
