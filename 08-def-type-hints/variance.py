from collections.abc import Callable


def update(  # 接收两个Callable作为参数
    probe: Callable[[], float],  # probe必须是一个无任何参数并返回float的可调用对象(callable)。
    display: Callable[[float], None],  # display接收一个float返回，并返回None
) -> None:
    temerature = probe()  # 调用probe
    # 想想这里有很多控制代码
    display(temerature)


def probe_ok() -> int:  # probe_ok与Callable[[], float]相容，因为返回 int 值对预期 float 值的代码没有影响。
    return 42


# display_wrong与Callable[[float], None]不相容，因为预期 int 参数的函数不一定能处理 float 值。
# 比如Python 函数hex 接受 int 值，但是拒绝 float 值。
def display_wrong(temperature: int) -> None:
    print(hex(temperature))


update(
    probe_ok, display_wrong
)  # Mypy 对这一行报错，因为 display_wrong 与 update 函数的display 参数的类型提示不相容


def display_ok(
    temperature: complex,
) -> None:  # display_ok 与 Callable[[float], None] 相容，因为接受complex 值的函数也能处理 float 参数。
    print(temperature)


update(probe_ok, display_ok)  # OK

"""
 $ mypy variance.py 
variance.py:24: error: Argument 2 to "update" has incompatible type "Callable[[int], None]"; expected "Callable[[float], None]"  [arg-type]
Found 1 error in 1 file (checked 1 source file)


综上所述，如果预期接受返回 float 值的回调，则提供返回 int 值的回调是可以的，因为在预期 float 值的地方都能使用 int 值。

正式地说，Callable[[], int] 是 Callable[[], float] 的子类型，因为 int 是 float 的子类型。
这意味着，那个 Callable 的返回值类型经历了协变（covariant），因为 int 和 float 之间具有子类型关系，而且变化方向与 Callable 类型中返回值的类型变化方向相同。

反过来，如果回调预期处理 float 值，却提供接受 int 参数的回调，则会导致类型错误。

正式地说，Callable[[int], None] 不是 Callable[[float],None] 的子类型。
虽然 int 是 float 的子类型，但是在参数化Callable 类型中，关系是相反的，
即 Callable[[float], None]是 Callable[[int], None] 的子类型。
因此我们说，那个Callable 声明的参数类型经历了逆变（contravariant）。


目前，可以认为大多数参数化泛型是不变的，这样更容易理解。

如果声明 scores: list[float]，就只能把list[float] 值赋给 scores，不能使用声明为 list[int] 或list[complex] 的对象。

* 不接受 list[int] 对象的原因是，scores 中不能存放float 值，而代码可能需要这么做。
* 不接受 list[complex] 对象的原因是，代码可能需要排序scores，找出中位数，而 complex 未提供 __lt__，所以list[complex] 不可排序。
"""
