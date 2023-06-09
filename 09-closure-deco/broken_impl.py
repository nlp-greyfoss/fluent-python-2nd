def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        count += 1
        total += new_value
        return total / count

    return averager


"""
>>> from broken_impl import make_averager
>>> avg = make_averager()
>>> avg(10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/workspaces/fluent-python-2nd/09-closure-deco/broken_impl.py", line 6, in averager
    count += 1
UnboundLocalError: local variable 'count' referenced before assignment

问题在于 count += 1 等价于 count = count + 1，当count是数字或其他不可变类型时。
所以我们实际做的是在averager中为count赋值，然后将它变成一个局部变量，同理total也一样。

所以对于不可变类型，我们唯一能做的是读取，而不能更新。
"""
