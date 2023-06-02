import sys
import re
import unicodedata
from collections.abc import Iterator

RE_WORD = re.compile(r"\w+")
STOP_CODE = sys.maxunicode + 1


def tokenize(text: str) -> Iterator[str]:  # 这是一个生成器函数
    """return iterabale of uppercased words"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()


def name_index(start: int = 32, end: int = STOP_CODE) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}  # 局部变量也可以添加注解
    for char in (chr(i) for i in range(start, end)):
        if name := unicodedata.name(char, ""):  # 使用海象运算符将结果保存到name，并判断name是否为空(字符串)
            for word in tokenize(name):
                index.setdefault(word, set()).add(char)

    return index


"""
$ mypy charindex.py 
Success: no issues found in 1 source file
>>> from charindex import name_index
>>> name_index(32, 65)
{'SPACE': {' '}, 'EXCLAMATION': {'!'}, 'MARK': {'!', '?', '"'}, 'QUOTATION': {'"'}, 'NUMBER': {'#'}, 'SIGN': {'<', '$', '=', '#', '+', '%', '>'}, 'DOLLAR': {'$'}, 'PERCENT': {'%'}, 'AMPERSAND': {'&'}, 'APOSTROPHE': {"'"}, 'LEFT': {'('}, 'PARENTHESIS': {')', '('}, 'RIGHT': {')'}, 'ASTERISK': {'*'}, 'PLUS': {'+'}, 'COMMA': {','}, 'HYPHEN': {'-'}, 'MINUS': {'-'}, 'FULL': {'.'}, 'STOP': {'.'}, 'SOLIDUS': {'/'}, 'DIGIT': {'3', '4', '5', '7', '2', '9', '0', '8', '1', '6'}, 'ZERO': {'0'}, 'ONE': {'1'}, 'TWO': {'2'}, 'THREE': {'3'}, 'FOUR': {'4'}, 'FIVE': {'5'}, 'SIX': {'6'}, 'SEVEN': {'7'}, 'EIGHT': {'8'}, 'NINE': {'9'}, 'COLON': {':'}, 'SEMICOLON': {';'}, 'LESS': {'<'}, 'THAN': {'<', '>'}, 'EQUALS': {'='}, 'GREATER': {'>'}, 'QUESTION': {'?'}, 'COMMERCIAL': {'@'}, 'AT': {'@'}}
>>> index = name_index(32, 65)
>>> index['SIGN']
{'<', '$', '=', '#', '+', '%', '>'}
>>> index['DIGIT']
{'3', '4', '5', '7', '2', '9', '0', '8', '1', '6'}
>>> index['DIGIT'] & index['EIGHT']
{'8'}
"""
