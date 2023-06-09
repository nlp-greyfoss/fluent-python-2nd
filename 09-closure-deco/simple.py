def deco(func):
    def inner():
        print("running inner()")

    return inner  # deco 返回它的inner函数对象


@deco
def target():  # target由deco装饰
    print("running target()")


target()  # 调用被装饰的target，实际运行的是inner
print(target)  # 查看对象，发现target现在是inner的引用。

"""
running inner()
<function deco.<locals>.inner at 0x7f160679d5a0>


装饰器是一个函数或另一个可调用对象；
装饰器可能用另一个函数替换被装饰的函数；
装饰器当模块被加载后马上执行；
"""
