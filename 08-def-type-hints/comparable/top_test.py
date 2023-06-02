from collections.abc import Iterator
from typing import TYPE_CHECKING

# TYPE_CHECKING 常量在运行(测试)时始终为 False，不过类型检查工具在做类型检查时会假装值为 True。

import pytest

from top import top


@pytest.mark.parametrize(
    "series, length, expected",
    [
        ((1, 2, 3), 2, [3, 2]),
        ((1, 2, 3), 3, [3, 2, 1]),
        ((3, 3, 3), 1, [3]),
    ],
)
def test_top(
    series: tuple[float, ...],
    length: int,
    expected: list[float],
) -> None:
    result = top(series, length)
    assert expected == result


def test_top_tuples() -> None:
    fruit = "mango pear apple kiwi banana".split()
    series: Iterator[tuple[int, str]] = (  # 为series声明类型，让mypy的输出更易懂
        (len(s), s) for s in fruit
    )
    length = 3
    expected = [(6, "banana"), (5, "mango"), (5, "apple")]
    result = top(series, length)
    if TYPE_CHECKING:  #  这个 if 语句禁止在运行测试时执行后面 3 行
        reveal_type(  # reveal_type() 不能在运行时调用，因为它不是常规函数，而是Mypy 提供的调试设施，因此无须使用 import 导入。
            series
        )  # reveal_type会输出一个调试信息
        reveal_type(expected)
        reveal_type(result)
    assert result == expected


# intentional type error
def test_top_objects_error() -> None:
    series = [object() for _ in range(4)]
    if TYPE_CHECKING:
        reveal_type(series)
    with pytest.raises(TypeError) as excinfo:
        top(series, 3)  # 该行会报错
    assert "'<' not supported" in str(excinfo.value)


"""
$ mypy top_test.py 
top_test.py:38: note: Revealed type is "typing.Iterator[Tuple[builtins.int, builtins.str]]" # 显示的是我们显式声明的类型
top_test.py:40: note: Revealed type is "builtins.list[Tuple[builtins.int, builtins.str]]" # 确认返回的类型是我们想要的
top_test.py:41: note: Revealed type is "builtins.list[Tuple[builtins.int, builtins.str]]"
top_test.py:49: note: Revealed type is "builtins.list[builtins.object]"
top_test.py:51: error: Value of type variable "LT" of "top" cannot be "object"  [type-var] # mypy发现了series中元素类型不能是object
Found 1 error in 1 file (checked 1 source file)


"""
