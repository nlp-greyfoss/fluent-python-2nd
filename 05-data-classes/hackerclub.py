from dataclasses import dataclass
from club import ClubMember

@dataclass
class HackerClubMember(ClubMember):  # 继承自ClubMember
    all_handles = set()              # all_handles 是类属性 
    handle: str = ''                 # handle 是str类型的实例字段，默认值为空字符串
    def __post_init__(self):
        cls = self.__class__         # 获取实例的class
        if self.handle == '':        # 如果为空字符串
            self.handle = self.name.split()[0] # 设置name的第一部分
        if self.handle in cls.all_handles:    # 如果handle存在
            msg = f'handle {self.handle!r} already exists.' #  则抛出异常
            raise ValueError(msg)
        cls.all_handles.add(self.handle)      # 增加新的handle到已存在的handle集合