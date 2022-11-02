from collections.abc import Iterable
from typing import TypeVar

from comparable import SupportsLessThan


LT = TypeVar('LT', bound=SupportsLessThan)

def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]