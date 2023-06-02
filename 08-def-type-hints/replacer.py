from collections.abc import Iterable

FromTo = tuple[str, str]  # 类型别名


def zip_replace(
    text: str, changes: Iterable[FromTo]
) -> str:  # 注意changes的类型注解，这里是Iterable类型，符合接收时要大方
    for from_, to in changes:
        text = text.replace(from_, to)
    return text


"""
>>> from replacer import zip_replace
>>> l33t = [('a', '4'), ('e', '3'), ('i', '1'), ('o', '0')]
>>> text = 'mad skilled noob powned leet'
>>> zip_replace(text, l33t)
'm4d sk1ll3d n00b p0wn3d l33t'
"""
