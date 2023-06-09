from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers


@singledispatch  # @singledispatch 标记的是处理 object 类型的基函数，是一个兜底方案
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f"<pre>{content}</pre>"


@htmlize.register  #  各个专门函数使用 @«base».register 装饰
def _(text: str) -> str:  # 如果第一个参数是str，专门函数的名称不重要，所以_是一个很好的选择
    content = html.escape(text).replace("\n", "<br/>\n")
    return f"<p>{content}</p>"


@htmlize.register  # 4 为每个需要特殊处理的类型注册一个函数，把第一个参数的类型提示设为相应的类型
def _(seq: abc.Sequence) -> str:
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>"


@htmlize.register  # singledispatch 支持使用 numbers 包中的抽象基类
def _(n: numbers.Integral) -> str:
    return f"<pre>{n} (0x{n:x})</pre>"


@htmlize.register  # bool 是 numbers.Integral 的子类型，但是 singledispatch逻辑会寻找与指定类型最匹配的实现，与实现在代码中出现的顺序无关
def _(n: bool) -> str:
    return f"<pre>{n}</pre>"


@htmlize.register(fractions.Fraction)  # 如果不想或者不能为被装饰的类型添加类型提示，则可以把类型传给@«base».register 装饰器
def _(x) -> str:
    frac = fractions.Fraction(x)
    return f"<pre>{frac.numerator}/{frac.denominator}</pre>"


@htmlize.register(decimal.Decimal)  #  @«base».register 装饰器会返回装饰之前的函数，因此可以叠放多个 register 装饰器，让同一个实现支持两个或更多类型
@htmlize.register(float)
def _(x) -> str:
    frac = fractions.Fraction(x).limit_denominator()
    return f"<pre>{x} ({frac.numerator}/{frac.denominator})</pre>"
