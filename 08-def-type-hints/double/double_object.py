def double(n: object) -> object:
    return n * 2


"""
$ mypy double_object.py 
double_object.py:2: error: Unsupported operand types for * ("object" and "int")  [operator]
Found 1 error in 1 file (checked 1 source file)
虽然上面的写法表示的和Any类型是同样的意思，但mypy会报错，因为object不支持__mu__方法。
"""

