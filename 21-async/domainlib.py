import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional

class Result(NamedTuple): # 命名元组可读性和可调试性更好
    domain: str
    found: bool

OptionalLoop = Optional[asyncio.AbstractEventLoop] # 类型别名 防止下一行太长

async def probe(domain: str, loop: OptionalLoop = None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)

async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]: # 返回一个异步声词器，可以被注解为AsyncIterator[类型]
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro # 在协程上await，并检索结果
        yield result # 使得该函数编变成异步生成器(结合async)