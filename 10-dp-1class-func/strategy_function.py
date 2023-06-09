from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import NamedTuple, Optional, Callable


class Customer(NamedTuple):
    name: str
    fidelity: int  # 积分


class LineItem(NamedTuple):  # 单个订单
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


# dataclass简化类的定义和实例化，可以自动生成__init__、__repr__和__eq__等方法。
# 属性可以写成customer: Customer的形式
# frozen=True 表示该类是不可变类
@dataclass(frozen=True)
class Order:  # Context
    customer: Customer
    cart: Sequence[LineItem]  # 购物车
    promotion: Optional[
        Callable[["Order"], Decimal]
    ] = None  # 这个类型提示的意思是，promotion 既可以是 None，也可以是接收一个 Order 参数并返回一个 Decimal 值的可调用对象

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            # self.promotion作为实例属性，需要一个Order实例参数，即self
            discount = self.promotion(self)  # 用可调用对象 self.promotion，传入 self，计算折扣
        return self.total() - discount  # 减去折扣金额

    def __repr__(self):
        return f"<Order total: {self.total():.2f} due: {self.due():.2f}>"


def fidelity_promo(order: Order) -> Decimal:  # 每个策略都是函数
    """有 1000 或以上积分的顾客，每个订单享 5% 折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal("0.05")
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    """同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal("0.1")

    return discount


def large_order_promo(order: Order) -> Decimal:
    """订单中不同商品的数量达到 10 个或以上，享 7% 折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal("0.07")

    return Decimal(0)


"""
>>> from strategy_function import *
>>> joe = Customer('John Doe', 0) #  与simple_strategy一样的测试代码
>>> ann = Customer('Ann Smith', 1100)
>>> cart = [LineItem('banana', 4, Decimal('.5')),
...         LineItem('apple', 10, Decimal('1.5')),
...         LineItem('watermelon', 5, Decimal(5))]
>>> Order(joe, cart, fidelity_promo) #  为了把折扣策略应用到 Order 实例上，只需把促销函数作为参数传入即可
<Order total: 42.00 due: 42.00>
>>> Order(ann, cart, fidelity_promo)
<Order total: 42.00 due: 39.90>
>>> banana_cart = [LineItem('banana', 30, Decimal('.5')), LineItem('apple', 10, Decimal('1.5'))]
>>> Order(joe, banana_cart, bulk_item_promo) # 使用了不同的促销函数
<Order total: 30.00 due: 28.50>
>>> long_cart = [LineItem(str(item_code), 1, Decimal(1)) for item_code in range(10)]
>>> Order(joe, long_cart, large_order_promo)
<Order total: 10.00 due: 9.30>
>>> Order(joe, cart, large_order_promo)
<Order total: 42.00 due: 42.00>
"""
