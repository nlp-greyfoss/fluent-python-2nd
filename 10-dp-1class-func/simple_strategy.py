from abc import ABC, abstractclassmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional


class Customer(NamedTuple):
    name: str
    fidelity: int  # 积分


class LineItem(NamedTuple):  # 单个订单
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


class Order(NamedTuple):  # Context
    customer: Customer
    cart: Sequence[LineItem]  # 购物车
    promotion: Optional["Promotion"] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount  # 减去折扣金额

    def __repr__(self):
        return f"<Order total: {self.total():.2f} due: {self.due():.2f}>"


class Promotion(ABC):  # Strategy: 一个抽象基类
    @abstractclassmethod
    def discount(self, order: Order) -> Decimal:
        """返回折扣正数金额"""


class FidelityPromo(Promotion):  # 第一个具体策略
    """有 1000 或以上积分的顾客，每个订单享 5% 折扣"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal("0.05")
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromo(Promotion):  # 第二个具体策略
    """同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣"""

    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal("0.1")

        return discount


class LargeOrderPromo(Promotion):  # 第三个具体策略
    """订单中不同商品的数量达到 10 个或以上，享 7% 折扣"""

    def discount(self, order: Order) -> Decimal:
        # 集合推导式
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal("0.07")

        return Decimal(0)


"""
>>> from strategy0.py import *
>>> joe = Customer("John Doe", 0) # 两位顾客：joe 的积分是 0，ann 的积分是 1100。
>>> ann = Customer('Ann Smith', 1100)
>>> cart = (LineItem('banana', 4, Decimal('.5')), #  购物车中有 3 个商品
...     LineItem('apple', 10, Decimal('1.5')),
...     LineItem('watermelon', 5, Decimal(5)))
>>> 
>>> Order(joe, cart, FidelityPromo()) # FidelityPromo 未给 joe 提供折扣
<Order total: 42.00 due: 42.00>
>>> Order(ann, cart, FidelityPromo()) # ann 得到了 5% 折扣，因为她的积分超过 1000
<Order total: 42.00 due: 39.90>
>>> banana_cart = (LineItem('banana', 30, Decimal('.5')), # banana_cart 中有 30 把香蕉和 10 个苹果
...                LineItem('apple', 10, Decimal('1.5')))
>>> 
>>> Order(joe, banana_cart, BulkItemPromo()) # BulkItemPromo 为 joe 购买的香蕉优惠了 ￥1.5 
<Order total: 30.00 due: 28.50>
>>> long_cart = tuple(LineItem(str(sku), 1, Decimal(1)) for sku in range(10)) #  long_order 中有 10 个不同的商品，每个商品的价格为 ￥1.0
>>> Order(joe, long_cart, LargeOrderPromo()) # LargerOrderPromo 为 joe 的整个订单提供 7% 折扣
<Order total: 10.00 due: 9.30>
>>> Order(joe, cart, LargeOrderPromo())
<Order total: 42.00 due: 42.00>
"""
