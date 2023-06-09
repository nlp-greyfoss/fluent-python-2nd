from decimal import Decimal
from strategy_function import Order, Customer, LineItem
from strategy_function import (
    fidelity_promo,
    bulk_item_promo,
    large_order_promo,
)  # 导入促销函数，使得它在全局命名空间中可用

promos = [
    promo
    for name, promo in globals().items()  #  迭代 globals() 返回的字典中的各项
    if name.endswith("_promo")  # 只选择以 _promo 结尾的值
    and name != "best_promo"  #  过滤掉 best_promo 自身，防止调用 best_promo 时出现无限递归
]


def best_promo(order: Order) -> Decimal:  #
    return max(promo(order) for promo in promos)


if __name__ == "__main__":
    joe = Customer("John Doe", 0)
    ann = Customer("Ann Smith", 1100)
    cart = [
        LineItem("banana", 4, Decimal(".5")),
        LineItem("apple", 10, Decimal("1.5")),
        LineItem("watermelon", 5, Decimal(5)),
    ]
    banana_cart = [
        LineItem("banana", 30, Decimal(".5")),
        LineItem("apple", 10, Decimal("1.5")),
    ]
    long_cart = [LineItem(str(item_code), 1, Decimal(1)) for item_code in range(10)]
    print(Order(joe, long_cart, best_promo))
    print(Order(joe, banana_cart, best_promo))
    print(Order(ann, cart, best_promo))

"""
python best_strategy0.py 
<Order total: 10.00 due: 9.30>
<Order total: 30.00 due: 28.50>
<Order total: 42.00 due: 39.90>
"""
