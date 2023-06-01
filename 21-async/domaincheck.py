import asyncio
import sys
from keyword import kwlist

from domainlib import multi_probe


async def main(tld: str) -> None:
    tld = tld.strip(".")
    names = (kw for kw in kwlist if len(kw) <= 4)  # 生成长度最多为4的关键词
    domains = (f"{name}.{tld}".lower() for name in names)  # 基于给定的后缀生成域名
    print("FOUND\t\tNOT FOUND")
    print("=====\t\t=========")
    async for domain, found in multi_probe(domains):  #  在multi_probe(domains)上异步迭代
        indent = "" if found else "\t\t"
        print(f"{indent}{domain}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        asyncio.run(main(sys.argv[1]))  # 基于命令行参数运行main协程
    else:
        print("Please provide a TLD.", f"Example: {sys.argv[0]} COM.BR")

""" 运行效果
$ python ./domaincheck.py net
FOUND           NOT FOUND
=====           =========
not.net
none.net
def.net
or.net
if.net
true.net
in.net
for.net
                from.net
del.net
try.net
is.net
and.net
else.net
as.net
with.net
                elif.net
                pass.net
"""
