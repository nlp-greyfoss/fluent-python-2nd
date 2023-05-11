import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

import httpx
import tqdm # type: ignore

from flag2_common import main, DownloadStatus, save_flag

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str) -> bytes:  
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True) 
    resp.raise_for_status()

    return resp.read() 

async def download_one(client: httpx.AsyncClient, cc: str, base_url: str, semaphore: asyncio.Semaphore, verbose: bool) -> DownloadStatus:
    try:
        async with semaphore: # semaphore作为异步上下文管理器，所以程序整体不会阻塞，只有当semaphore为零时，协程会挂起
            image = await get_flag(client, base_url, cc)
    except httpx.HTTPStatusError as exc: # 错误处理
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        await asyncio.to_thread(save_flag, image, f"{cc}.gif") # 保存图像是一个I/O操作，为了避免阻塞event loop，通过这种方式，在线程中运行save_flag
        # Python3.9之前可以这么写：
        # loop = asyncio.get_running_loop()
        # loop.run_in_executor(None, save_flag, image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = "OK"
    
    if verbose and msg:
        print(cc, msg)
    return status

async def supervisor(cc_list: list[str], base_url: str, verbose: bool, concur_req: int) -> Counter[DownloadStatus]: # 协程方法
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req) # 创建一个不允许超过concur_req的活动协程的Semaphore
    async with httpx.AsyncClient() as client:
        to_do = [download_one(client, cc, base_url, semaphore, verbose) for cc in sorted(cc_list)] # 创建一个协程对象列表
        to_do_iter = asyncio.as_completed(to_do) # asyncio.as_completed是一个生成器，它生成协程序，按照它们完成的顺序返回传递给它的协程序的结果
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list)) # 显示精度条
        error: httpx.HTTPError | None = None # 保存抛出的异常
        for coro in to_do_iter: # 迭代完成的协程
            try:
                status = await coro  # 得到结果或异常，这里不会阻塞
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
                error = exc  # 保存异常
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                error = exc  # 保存异常
            except KeyboardInterrupt:
                break

            if error:
                status = DownloadStatus.ERROR # 将状态设成ERROR
                if verbose:
                    url = str(error.request.url) #  拿到url
                    cc = Path(url).stem.upper() #  拿到cc
                    print(f"{cc} error: {error_msg}") # 打印
            
            counter[status] += 1

        return counter

def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)

    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

        

