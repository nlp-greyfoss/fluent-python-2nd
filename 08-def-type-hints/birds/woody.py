from birds import *

woody = Bird()
alert(woody)
alert_duck(woody)
alert_bird(woody)

"""
$ mypy woody.py 
birds.py:19: error: "Bird" has no attribute "quack"  [attr-defined]
woody.py:5: error: Argument 1 to "alert_duck" has incompatible type "Bird"; expected "Duck"  [arg-type]
Found 2 errors in 2 files (checked 1 source file)

这次在运行时，这三个函数没有一个能执行成功
alert(woody):  AttributeError: 'Bird' object has no attribute 'quack'
alert_duck(woody):  AttributeError: 'Bird' object has no attribute 'quack'
alert_bird(woody): AttributeError: 'Bird' object has no attribute 'quack'
"""
