import asyncio
import socket

from keyword import kwlist

MAX_KEYWORD_LEN = 4 

async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop() # 获取运行的asyncio event loop的引用，如果没有运行的，则抛出异常。 而get_event_loop已被启用
    try:
        # 使用await 来避免阻塞，因为它会挂起当前的协程对象(比如当前的协程对象在等待服务器的返回)
        await loop.getaddrinfo(domain, None) # 会返回(family, type, proto, canonname, sockaddr)，但这里我们不关心它的返回值
    except socket.gaierror:
        return (domain, False)
    return (domain, True) 

async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN) # 产生Python关键词的生成器
    domains = (f"{name}.dev".lower() for name in names) # 产生带有.dev后缀的domain name生成器
    coros = [probe(domain) for domain in domains] # 构建协程对象列表，通过用domain参数调用probe协程
    for coro in asyncio.as_completed(coros): # asyncio.as_completed是一个生成器，它生成协程序，按照它们完成的顺序返回传递给它的协程序的结果
        domain, found = await coro # 此时，我们知道协程完成了，因此 这里的await不会阻塞
        mark = "+" if found else " "
        print(f"{mark} {domain}") # 返回元组就是为了这里好展示

if __name__ == '__main__':
    asyncio.run(main()) # 开启event loop，并且只会在event loop退出时返回。