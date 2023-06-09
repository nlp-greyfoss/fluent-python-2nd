import time
import functools


def clock(func):
    @functools.wraps(func)  # 会把__name__和__doc__属性从func复制到clocked中
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)  # 现在可以接收关键字参数
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_lst)
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result

    return clocked
