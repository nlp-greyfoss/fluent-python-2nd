# 重构策略模式


## 经典的策略模式


![image-20230609092518850](https://images-1253469118.cos.ap-guangzhou.myqcloud.com/dataimage-20230609092518850.png)

策略模式： 定义一系列算法，把它们一一封装起来，并且使它们可以相互替换。策略模式使得算法可以独立于使用它的客户而变化。

假设某网点有这样的折扣策略：
* 有 1000 或以上积分的顾客，每个订单享 5% 折扣。
* 同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣。
* 订单中不同商品的数量达到 10 个或以上，享 7% 折扣。

为了简化，假设这些折扣策略不能叠加。

策略模式见上图，涉及到以下内容：

* 上下文(Context)
    * 提供一个服务，把一些计算委托给实现不同算法的可互换组件。在这个电商示例中，上下文是 Order，它根据不同的算法计算促销折扣。
* 策略(Strategy)
    * 实现不同算法的组件共同的接口。在这个示例中，名为Promotion 的抽象类扮演这个角色。
* 具体策略(Concrete strategy)
　　策略的具体子类。FidelityPromo、BulkPromo 和LargeOrderPromo 是这里实现的 3 个具体策略。

实现见simple_strategy.py，该示例可以实现功能。但如果把函数当做对象使用，那么实现同样的功能所需的代码更少。


## 使用函数实现策略模式

在上一节中每个具体策略类只有一个方法，并且没有状态。所以看起来就像普通函数。因此，这里我们用简单函数来替代，并移除抽象基类。
见strategy_function.py

## 选择最佳策略的简单方式

现在，我们来实现简单的策略选择。即遍历所有策略，选择折扣最多的一个。
```py
>>> from strategy_function import *
>>> promos = [fidelity_promo, bulk_item_promo, large_order_promo] # 所有的策略
>>> def best_promo(order: Order) -> Decimal: # order作为参数，返回计算出来的最佳折扣
...     return max(promo(order) for promo in promos)
... 

>>> joe = Customer('John Doe', 0)
>>> ann = Customer('Ann Smith', 1100)
>>> cart = [LineItem('banana', 4, Decimal('.5')), LineItem('apple', 10, Decimal('1.5')), LineItem('watermelon', 5, Decimal(5))]
>>> banana_cart = [LineItem('banana', 30, Decimal('.5')), LineItem('apple', 10, Decimal('1.5'))]
>>> long_cart = [LineItem(str(item_code), 1, Decimal(1)) for item_code in range(10)]
>>>
>>> Order(joe, long_cart, best_promo) # best_promo 为顾客 joe 选择 larger_order_promo
<Order total: 10.00 due: 9.30>
>>> Order(joe, banana_cart, best_promo) #  订购大量香蕉时，joe 使用 bulk_item_promo 提供的折扣
<Order total: 30.00 due: 28.50>
>>> Order(ann, cart, best_promo) # 在一个简单的购物车中，best_promo 为忠实顾客 ann 提供fidelity_promo 优惠的折扣
<Order total: 42.00 due: 39.90>
```

## 找出一个模块中的全部策略

上面我们通过`promos = [fidelity_promo, bulk_item_promo, large_order_promo]`定义出了所有的策略有点傻，我们希望代码能自动找到这些策略。以便方便以后我们添加新的策略。

在Python中，模块也是一等对象，且标准库提供了几个处理这些模块的函数。内置函数`globals()`返回一个字典，表示当前的全局符号表。
这个符号表始终针对当前模块(对函数或方法来说，指定义它们的模块，而不是调用它们的模块)。

我们即利用该内置函数来实现，第一个版本见best_strategy0.py，但是还是要显示导入促销函数，一种解决方法是`import *`。


还有一种做法是把所有的策略放到同一类中，比如promotions.py中，然后利用`inspect.getmembers`来获取promotions模块的属性。见best_strategy1.py。
这样不管怎样的命名策略都可以用，但有一个唯一的隐性要求是：只能在里面写计算订单折扣的策略函数。

动态收集促销折扣函数的一种更显示的方案是使用简单的装饰器。

# 使用装饰器改进策略模式


见best_strategy.py和best_strategy2.py


# 命令模式

在最后的这个小节讨论命令模式，并通过函数来实现。

![image-20230609142745753](https://images-1253469118.cos.ap-guangzhou.myqcloud.com/dataimage-20230609142745753.png)

菜单驱动的文本编辑器的 UML 类图，使用命令设计模式实现。各个命令可以有不同的接收者，即实现操作的对象。对PasteCommand 来说，接收者是 Document；对 OpenCommand 来说，接收者是应用程序。

命令模式的目的是解耦调用操作的对象（调用者）和提供实现的对象（接收者）。在二者之间放一个Command对象，它实现只有一个方法的接口，调用接收者中的方法执行所需的操作。
这样，调用者无须了解接收者的接口，而且不同的接收者可以适应不同的Command子类。 注意， MacroCommand 可能会保存一系列命令。

可以不为调用者提供 Command 实例，而是给它一个函数。此时，调用者不调用 command.execute()，而是直接调用 command()。

MacroCommand 可以通过定义了 __call__ 方法的类实现。这样，MacroCommand 的实例就是可调用对象，各自维护着一个函数列表，供以后调用。

```py
 """A command that executes a list of commands"""
 class MacroCommand:
    def __init__(self, commands):
        self.commands = list(commands) # 根据 commands 参数构建一个列表，这样能确保参数是可迭代对象，还能在各个 MacroCommand 实例中保存各个命令引用的副本

    def __call__(self):
        for command in self.commands:  # 调用 MacroCommand 实例时，self.commands 中的各个命令依序执行
            command()
```

这里采用的方式与策略模式所用的方式类似：把实现单方法接口的类的实例替换成可调用对象。毕竟，每个 Python 可调用对象都实现了单方法接口，这个方法就是 `__call__`。

