from typing import Protocol, Any


class SupportsLessThan(Protocol):  # 是Protocol的子类
    def __lt__(self, other: Any) -> bool:  # 它的方法体是 ...
        ...
