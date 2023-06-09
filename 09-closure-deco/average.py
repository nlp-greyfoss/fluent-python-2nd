def make_averager():
    series = []  # 是make_averager的局部变量，因为赋值语句在make_averager的主体中
    # 但，调用avg(10)时，make_averager函数已经返回，它的局部作用域就消失了。
    # 在averager函数中，series是自由变量，指未在局部作用域中绑定的变量。
    #
    # 可以发现在__code__属性中保持的局部变量和自由变量的名称
    # >>> avg.__code__.co_varnames
    # ('new_value', 'total')
    # >>> avg.__code__.co_freevars
    # ('series',)
    # series 的值在返回的 avg 函数的 __closure__ 属性中
    # >>> avg.__closure__
    # (<cell at 0x7f9fcb729870: list object at 0x7f9fcb64fc00>,)
    # >>> avg.__closure__[0].cell_contents
    # [10, 11, 15]

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager


"""
>>> from average import make_averager
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(15)
12.0
"""
