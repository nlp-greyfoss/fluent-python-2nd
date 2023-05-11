import asyncio
from httpx import AsyncClient
from flags import BASE_URL, save_flag, main

def download_many(cc_list: list[str]) -> int: 
    return asyncio.run(supervisor(cc_list))  # 执行 event loop 运行协程 supervisor，直到它返回。当event loop运行时，会阻塞

async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client: # 这是一个异步的上下文管理器
        to_do = [download_one(client, cc) for cc in sorted(cc_list)] # 构建协程列表
        res = await asyncio.gather(*to_do) # 等待asyncio.gather协程，它接收awaitable参数，并等待它们完成，以提交顺序返回它们的结果
    
    return len(res) # 返回完成结果列表的长度


async def download_one(client: AsyncClient, cc: str): # 它必须是协程方法，才能await调用协程get_flag
    image = await get_flag(client, cc)
    save_flag(image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc

async def get_flag(client: AsyncClient, cc: str) -> bytes: 
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True) # 该方法返回的ClientResponse对象也是一个异步上下文管理器

    return resp.read() # 网络I/O操作都作为协程方法实现，所以它们由event loop异步地处理

if __name__ == "__main__":
    main(download_many)

