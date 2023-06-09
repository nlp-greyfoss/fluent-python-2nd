from decimal import Decimal

from strategy_function import Order, Customer, LineItem
from best_strategy2 import promos
import promotions  # 让该模块加载


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

"""$ python best_strategy.py
add <function fidelity_promo at 0x7f5a6ee58a60>
add <function bulk_item_promo at 0x7f5a6ee58c10>
add <function large_order_promo at 0x7f5a6ee58ca0>
<Order total: 10.00 due: 9.30>
<Order total: 30.00 due: 28.50>
<Order total: 42.00 due: 39.90>

"""
