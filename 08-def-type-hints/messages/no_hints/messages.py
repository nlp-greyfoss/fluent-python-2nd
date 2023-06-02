from typing import Optional

# def show_count(count: int, word: str) -> str:
#    if count == 1:
#        return f"1 {word}"
#    count_str = str(count) if count else "no"
#    return f"{count_str} {word}s"


# plural: str | None 可以为str或None 等同于 Optional[str] = None
def show_count(count: int, singular: str, plural: str | None) -> str:
    if count == 1:
        return f"1 {singular}"
    count_str = str(count) if count else "no"
    if not plural:
        plural = singular + "s"
    return f"{count_str} {plural}"


"""
# 如果函数签名没有注解，默认不会报错
$ mypy messages/no_hints/messages.py
Success: no issues found in 1 source file
"""
