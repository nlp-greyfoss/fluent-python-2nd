from contextlib import asynccontextmanager
import asyncio


@asynccontextmanager
async def web_page(url):  # @asynccontextmanager注解的函数必须是异步生成器
    loop = asyncio.get_running_loop()  # 使用get_running_loop而不是get_event_loop
    data = await loop.run_in_executor(
        None, download_webpage, url
    )  # 假设download_webpage是一个阻塞函数，这里再其他的线程中运行防止阻塞event loop

    yield data  # 所有yield表达式之前的代码会到`__aenter__`协程方法中 data的值将绑定到下面async with语句中as子句之后的data变量。

    await loop.run_in_executor(None, update_stats, url)  # 在yield之后的代码会到`__aexit__`中


# 使用async with 来调用 web_page
async with web_page("google.com") as data:
    process(data)
