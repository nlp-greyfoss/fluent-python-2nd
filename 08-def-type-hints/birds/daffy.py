from birds import *

daffy = Duck()
alert(daffy)  # 有效调用，因为alert没有类型提示
alert_duck(daffy)  # 有效调用，因为alert_duck接收Duck类型，且daffy是Duck
alert_bird(daffy)  # 有效调用，因为alert_bird接收Bird类型，且daffy也是Bird


"""
$ mypy birds/daffy.py 
birds/birds.py:19: error: "Bird" has no attribute "quack"  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
虽然抛出这个错误，但这三个函数本身是OK的。
"""

"""
$ python birds/daffy.py 
Quack!
Quack!
Quack!
"""
