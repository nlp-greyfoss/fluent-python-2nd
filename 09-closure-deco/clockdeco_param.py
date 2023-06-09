import time


DEFAULT_FMT = "[{elapsed:0.8f}s] {name}({args}) -> {result}"  # 多了格式化功能


def clock(fmt=DEFAULT_FMT):  # clock现在是参数化装饰器工厂函数
    def decorate(func):  # decorate是真正的装饰器
        def clocked(*_args):  # clocked 保证被装饰的函数
            t0 = time.perf_counter()
            _result = func(*_args)  # 是被装饰的函数返回的真正结果
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ", ".join(
                repr(arg) for arg in _args
            )  #  _args 用于存放 clocked 的真正参数，args 是用于显示的字符串。
            result = repr(_result)  # result 是 _result 的字符串表示形式，用于显示
            print(
                fmt.format(**locals())
            )  # 这里使用 **locals() 是为了在 fmt 中引用 clocked 的局部变量，即编译器抱怨的那些未使用的变量：elapsed,name,args,result
            return _result  # clocked 将取代被装饰的函数，因此它应该返回被装饰的函数返回的值

        return clocked  # decorate 返回 clocked

    return decorate  # clock 返回 decorate


if __name__ == "__main__":

    @clock()  # 不传入参数，使用默认的格式字符串
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(0.123)

"""
 $ python clockdeco_param.py 
[0.12319530s] snooze(0.123) -> None
[0.12328470s] snooze(0.123) -> None
[0.12322180s] snooze(0.123) -> None
"""
