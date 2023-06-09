from typing import Callable
from decimal import Decimal
from strategy_function import Order

Promotion = Callable[[Order], Decimal]

promos: list[Promotion] = []  # promos 列表位于模块全局命名空间中，起初是空的


def promotion(promo: Promotion) -> Promotion:  # 装饰器
    print(f"add {promo}")
    promos.append(promo)  # 加入promos列表
    return promo  # 返回它自己
