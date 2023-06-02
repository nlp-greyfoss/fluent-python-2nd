# 注解中可用的类型

Postel定律： 接收时要大方，发送时要保守。 接收参数时要抽象，返回时要具体。

大部分Python类型可以在类型提示中使用，但有一些限制和建议。
可用于注解的类型：
* typing.Any
* 简单的类型和类： 比如`int,float,str,bytes`以及标准库，第三方库和用户定义的类。
  *  `int`与`float`相容，`float`与`complex`相容，所以`int`与`complex`相容。从受支持的操作可以解释。
* typing.Optional 和 typing.Union
* 泛化容器, 包括 元组 和 映射 
  *  比如`list[str]`
  *  元组： `tuple[str, float, str]` 详见coordinates目录
  *  映射： 使用形式`MappingType[KeyType, ValueType]`注解，见charindex.py
* 抽象基类
  *  `from collections.abc import Mapping`
* 泛化可迭代对象 `Sequence`和`Iterable`等是非常适用于作为参数类型的。 见replacer.py
* 参数化泛型和TypeVar 
  *  参数化泛型像 `list[T]` 见sample.py
  *  TypeVar是T的定义，不能像Java那样直接写T
  *  受限TypeVar 见mode_hashable.py
  *  `AnyStr = TypeVar('AnyStr', bytes, str)` 是一个`typing`模块预定义的TypeVar，可以用于任何接收bytes或str的函数中。
* typing.Protocols 见comparable目录
* typing.Callable  它的形式是`Callable[[ParamType1, ParamType2], ReturnType]`，且参数列表，即这里的 `[ParamType1, ParamType2]`，可以包含零或多个类型
  * 泛化类型参数与类型层次结构的交互引入了一个新类型概念：型变（variance） 见variance.py
* typing.NoReturn 该特殊类型仅用于注解绝不返回的函数的返回值类型。这类函数通常会抛出异常，比如`sys.exit()`会抛出`SystemExit`终止Python进程。

## Any

### 子类型与相容

```py
class T1:
 ...
class T2(T1):
 ...
def f1(p: T1) -> None:
 ...
o2 = T2()
f1(o2) # OK
```

`f1(o2)`的调用运用了里氏替换原则。可以从受支持的操作(supported operation)角度定义子类型：用`T2`类型对象替换`T1`类型的对象，如果程序的行为仍然正确，那么`T2`就是`T1`的子类型。

在渐进式类型系统中还有一种关系：相容(consistent-with)。满足子类型关系必定相容的，不过对`Any`还有特殊的规定。

相容规则如下：
1. 对`T1`及其子类型`T2`，`T2`与`T1`相容(里氏替换)。
2. 任何类型都与`Any`相容：声明为`Any`类型的参数接受任何类型的对象。
3. `Any`与任何类型都相容： 始终可以把`Any`类型的对象传给预期其他类型的参数。


针对注解数字参数有以下几种选择：
* 使用`int`,`float`或`complex`中的某个具体类型
* 声明一种联合类型，如`Union[float, Decimal, Fraction]`
* 也可以使用`SupportsFloat`等数字协议

d
