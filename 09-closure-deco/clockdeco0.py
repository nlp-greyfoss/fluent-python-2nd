import time


def clock(func):
    """
    simple decorator to show the running of functions
    """

    def clocked(*args):  # 接收任意数量的位置参数
        t0 = time.perf_counter()
        result = func(*args)  # 这行是没问题的，因为clocked的闭包中包含func
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result

    return clocked  # 返回内部函数替换原来被装饰的函数


