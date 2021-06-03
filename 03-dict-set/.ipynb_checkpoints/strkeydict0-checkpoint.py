class StrKeyDict0(dict):  # 继承dict

    def __missing__(self, key):
        if isinstance(key, str):  # 如果缺失键本身就是str，则抛出KeyError异常
            raise KeyError(key)
        return self[str(key)]  # 否则转换为str再查找

    def get(self, key, default=None):
        try:
            return self[key]  # self[key]把查找委托给__getitem__，这样在宣布查找失败之前，还能通过__missing__再给某个键一个机会
        except KeyError:
            return default  # 如果抛出KeyError，那么说明__missing__也失败了，于是返回默认值

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()  # 先按照传入键的原本值查找，如果没找到，再用str()方法把键转换成str再查找一次