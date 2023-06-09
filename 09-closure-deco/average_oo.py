class Averager:
    """
    一个计算不断增加的系列值的平均值的类，初学者可能会这么实现。average.py中给出了函数式的实现。
    """

    def __init__(self) -> None:
        self.series = []

    def __call__(self, new_value) -> float:
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)


"""
>>> from average_oo import Averager
>>> avg = Averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
"""
