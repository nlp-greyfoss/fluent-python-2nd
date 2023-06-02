from collections.abc import Sequence


def columnize(
    sequence: Sequence[str], num_columns: int = 0
) -> list[tuple[str, ...]]:  # tuple[str, ...] 表示不定长的tuple，元素都为str
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]


"""
$ mypy columnize.py 
Success: no issues found in 1 source file
$ python
Python 3.10.4 (main, Mar 13 2023, 19:44:25) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from columnize import columnize
>>> animals = 'drake fawn heron ibex koala lynx tahr xerus yak zapus'.split()
>>> table = columnize(animals)
>>> table
[('drake', 'koala', 'yak'), ('fawn', 'lynx', 'zapus'), ('heron', 'tahr'), ('ibex', 'xerus')]
>>> for row in table:
...     print(''.join(f'{word:10}' for word in row))
... 
drake     koala     yak       
fawn      lynx      zapus     
heron     tahr      
ibex      xerus     
"""
