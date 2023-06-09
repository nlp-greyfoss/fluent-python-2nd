registry = []  # 用于保存@register装饰的函数


def register(func):  # 以函数作为参数
    print(f"running register ({func})")  # 显示哪个函数被装饰了
    registry.append(func)  # 保存到registry中
    return func  # 返回函数： 我们必须要返回一个函数，这里返回的是接收到的函数


@register  # f1和f2被@register装饰
def f1():
    print("running f1()")


@register
def f2():
    print("running f2()")


def f3():  # f3没有
    print("running f3()")


def main():  # 打印registry信息，然后执行f1,f2,f3
    print("running main()")
    print("registry ->", registry)
    f1()
    f2()
    f3()


if __name__ == "__main__":
    main()

"""
 $ python registration.py 
running register (<function f1 at 0x7fde71691510>)
running register (<function f2 at 0x7fde716915a0>)
running main()
registry -> [<function f1 at 0x7fde71691510>, <function f2 at 0x7fde716915a0>]
running f1()
running f2()
running f3()
"""
