import functools
from clockdeco import clock


@functools.cache  # Python3.9后支持
@clock  # 这是一个叠加装饰器的例子：@cache应用到了@clock返回的函数上
"""
类似cache(clock(fibonacci)) 即先应用clock，然后它的返回值传递给cache
"""
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == "__main__":
    print(fibonacci(6))

"""
没用cache的示例，可以看到，有很多重复计算。
$ python fibo_demo.py 
[0.00000090s] fibonacci(0) -> 0
[0.00000070s] fibonacci(1) -> 1
[0.00004880s] fibonacci(2) -> 1
[0.00000070s] fibonacci(1) -> 1
[0.00000540s] fibonacci(0) -> 0
[0.00000070s] fibonacci(1) -> 1
[0.00003050s] fibonacci(2) -> 1
[0.00005490s] fibonacci(3) -> 2
[0.00012670s] fibonacci(4) -> 3
[0.00000040s] fibonacci(1) -> 1
[0.00000070s] fibonacci(0) -> 0
[0.00000070s] fibonacci(1) -> 1
[0.00002360s] fibonacci(2) -> 1
[0.00004540s] fibonacci(3) -> 2
[0.00000040s] fibonacci(0) -> 0
[0.00000060s] fibonacci(1) -> 1
[0.00002330s] fibonacci(2) -> 1
[0.00000060s] fibonacci(1) -> 1
[0.00000050s] fibonacci(0) -> 0
[0.00000060s] fibonacci(1) -> 1
[0.00002410s] fibonacci(2) -> 1
[0.00004760s] fibonacci(3) -> 2
[0.00009390s] fibonacci(4) -> 3
[0.00016240s] fibonacci(5) -> 5
[0.00031280s] fibonacci(6) -> 8
8

在加了@chache装饰器后：
$ python fibo_demo.py 
[0.00000060s] fibonacci(0) -> 0
[0.00000070s] fibonacci(1) -> 1
[0.00006160s] fibonacci(2) -> 1
[0.00000140s] fibonacci(3) -> 2
[0.00008790s] fibonacci(4) -> 3
[0.00000120s] fibonacci(5) -> 5
[0.00011370s] fibonacci(6) -> 8
8
"""
