import asyncio
import socket
from collections.abs import Iterable, AsyncIterator
from typing import NamedTuple, Optional

class Result(NamedTuple): # 1
    domain: str
    found: bool

OptionalLoop = Optional[asyncio.AbstractEventLoop] # 2

async def probe(domain: str, loop: OptionalLoop = None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)

async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro #
        yield result