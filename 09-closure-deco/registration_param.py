registry = set()  # 现在是一个set


def register(active=True):  # 接受一个可选的关键词参数
    def decorate(func):  # 内部函数decorate是真正的装饰器，它的参数是一个函数
        print(f"running register(active={active})->decorate({func})")
        if active:  # 为True时才注册func
            registry.add(func)
        else:
            registry.discard(func)  # 否则把它删除

        return func

    return decorate


@register(active=False)  # 工厂函数必须作为函数调用，并传入所需的参数
def f1():
    print("running f1()")


@register()  # 即使不传入参数，也需要作为函数调用，返回真正的装饰器decorate
def f2():
    print("running f2()")


def f3():  # f3没有
    print("running f3()")


"""
>>> import registration_param
running register(active=False)->decorate(<function f1 at 0x7fe861d27ac0>)
running register(active=True)->decorate(<function f2 at 0x7fe861d27b50>)
>>> registration_param.registry
{<function f2 at 0x7fe861d27b50>}
可以看到，只有f2出现在了registry中。


>>> from registration_param import *
running register(active=False)->decorate(<function f1 at 0x7f0ecd0e3ac0>)
running register(active=True)->decorate(<function f2 at 0x7f0ecd0e3b50>)
>>> registry # 导入这个模块时，f2在registry中
{<function f2 at 0x7f0ecd0e3b50>}
>>> register()(f3) # 应用到f3上
running register(active=True)->decorate(<function f3 at 0x7f0ecd0e3a30>)
<function f3 at 0x7f0ecd0e3a30>
>>> registry # 可以看到多了f3
{<function f3 at 0x7f0ecd0e3a30>, <function f2 at 0x7f0ecd0e3b50>}
>>> register(active=False)(f2) # 从regisgry中删除f2
running register(active=False)->decorate(<function f2 at 0x7f0ecd0e3b50>)
<function f2 at 0x7f0ecd0e3b50>
>>> registry # f2不见了
{<function f3 at 0x7f0ecd0e3a30>}
"""
