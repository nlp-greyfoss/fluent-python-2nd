b = 6  # 步骤②中定义


def f1(a):
    print(a)
    print(b)


f1(3)

"""
①
3
Traceback (most recent call last):
  File "/workspaces/fluent-python-2nd/09-closure-deco/test_scope.py", line 6, in <module>
    f1(3)
  File "/workspaces/fluent-python-2nd/09-closure-deco/test_scope.py", line 3, in f1
    print(b)  # b未定义
NameError: name 'b' is not defined
"""

# ② 如果在全局定义b，然后调用f1:
"""
$ python test_scope.py 
3
6
"""


"""
再看一个例子，这次print(b)未执行，第一个看到时，觉得至少print(b)会先执行。
但当Pythoh编译函数体时，它认为b是一个局部变量，因为b是在函数内定义的。
这样，Python会尝试从局部作用域中获取b，后面调用f2(3)时，f2的主体顺利获取并打印局部变量a的值，
但在尝试获取局部变量b的值时，发现b没有绑定值。

Python不要求声明变量，但假定在函数主体中赋值的变量是局部变量。


>>> b = 6
>>> def f2(a):
...     print(a)
...     print(b)
...     b = 9
... 
>>> f2(3)
3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in f2
UnboundLocalError: local variable 'b' referenced before assignment
"""

# 在函数中赋值时，如果想让解释器把b当成全局变量，为它分配一个新值，就要使用global声明。
"""
>>> b = 6
>>> def f3(a):
...     global b
...     print(a)
...     print(b)
...     b = 9
... 
>>> f3(3)
3
6
>>> b
9
"""
