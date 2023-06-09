# from clockdeco0 import clock
from clockdeco import clock
import time


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == "__main__":
    print("*" * 40, "Calling snooze(.123)")
    snooze(0.123)
    print("*" * 40, "Calling factorial(6)")
    print("6! =", factorial(6))


"""
$ python clockdeco_demo.py 
**************************************** Calling snooze(.123)
[0.12325290s] snooze(0.123) -> None
**************************************** Calling factorial(6)
[0.00000060s] factorial(1) -> 1
[0.00003180s] factorial(2) -> 2
[0.00005230s] factorial(3) -> 6
[0.00008500s] factorial(4) -> 24
[0.00010090s] factorial(5) -> 120
[0.00011900s] factorial(6) -> 720
6! = 720

调用factorial(n)相当于调用clocked(n)

这是装饰器的典型作用：把被装饰的函数替换成新函数，新函数接受的参数与被装饰的函数一样，而且（通常）会返回被装饰的函数本该返回的值，同时还会做一些额外操作。
"""
