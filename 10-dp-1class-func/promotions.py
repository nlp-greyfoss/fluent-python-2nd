from decimal import Decimal

from strategy_function import Order
from best_strategy2 import promotion


@promotion
def fidelity_promo(order: Order) -> Decimal:  # 每个策略都是函数
    """有 1000 或以上积分的顾客，每个订单享 5% 折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal("0.05")
    return Decimal(0)


@promotion
def bulk_item_promo(order: Order) -> Decimal:
    """同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal("0.1")

    return discount


@promotion
def large_order_promo(order: Order) -> Decimal:
    """订单中不同商品的数量达到 10 个或以上，享 7% 折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal("0.07")

    return Decimal(0)
