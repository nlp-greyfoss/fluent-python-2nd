from collections.abc import Iterable
from typing import TypeVar

from comparable import SupportsLessThan


LT = TypeVar("LT", bound=SupportsLessThan)


def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]


"""
series的类型限制应该是那些实现了__lt__方法的类型。我们可以类似typing.Hashable作为它的上限，但typing中没有类似的类型，
所以我们需要创建它。叫SupportsLessThan，见comparable.py

top 函数的 series 参数采用的注解方式想表达的意思是：“series 的名义类型无关紧要，只要实现 __lt__ 方法即可。
"""
