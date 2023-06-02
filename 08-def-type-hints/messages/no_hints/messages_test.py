from pytest import mark

from messages import show_count


@mark.parametrize(
    "qty, expected",
    [
        (1, "1 part"),
        (2, "2 parts"),
    ],
)
def test_show_count(qty, expected):
    got = show_count(qty, "part")
    assert got == expected


def test_show_count_zero():
    got = show_count(0, "part")
    assert got == "no parts"


# 为messages.py添加一个新函数，这里添加对应的测试
def test_irregulary() -> None:
    got = show_count(2, "child", "children")
    assert got == "2 children"


"""
--disallow-untyped-defs 可选项 禁止在函数或方法定义中省略参数和返回值的类型注释，这是一个很严格的限制。
$ mypy --disallow-untyped-defs messages/no_hints/messages_test.py 
messages/no_hints/messages.py:1: error: Function is missing a type annotation  [no-untyped-def]
messages/no_hints/messages_test.py:13: error: Function is missing a type annotation  [no-untyped-def]
messages/no_hints/messages_test.py:18: error: Function is missing a return type annotation  [no-untyped-def]
messages/no_hints/messages_test.py:18: note: Use "-> None" if function does not return a value
Found 3 errors in 2 files (checked 1 source file)
"""

"""
推荐使用另一个可选项 --disallow-incomplete-defs 禁止完全定义的类型  如果代码中存在未完全定义的注解，例如只定义了函数参数的类型但没有定义返回值类型，那么 mypy 就会产生错误。
如果完全没有定义注解，则不会报错。
$ mypy --disallow-incomplete-defs  messages/no_hints/messages_test.py 
Success: no issues found in 1 source file
"""


"""
如果修改messages.py中的代码，只添加一个返回类型注解
$ mypy --disallow-incomplete-defs  messages/no_hints/messages_test.py 
messages/no_hints/messages.py:1: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
Found 1 error in 1 file (checked 1 source file)

这样可以基于-disallow-incomplete-defs 可选项，逐渐为函数添加注解，而不影响未添加注解的函数。
"""
