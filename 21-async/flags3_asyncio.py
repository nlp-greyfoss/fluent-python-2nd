import httpx
from http import HTTPStatus

import asyncio

from flag2_common import main, DownloadStatus, save_flag

async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str) -> bytes:  
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True) 
    resp.raise_for_status()

    return resp.read() 

async def get_country(client: httpx.AsyncClient,
                        base_url: str,
                        cc: str) -> str: 
    url = f'{base_url}/{cc}/metadata.json'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    metadata = resp.json()  # 基于JSON内容构建一个字典
    return metadata['country'] # 返回country name

async def download_one(client: httpx.AsyncClient, cc: str, base_url: str, semaphore: asyncio.Semaphore, verbose: bool) -> DownloadStatus:
    try:
        async with semaphore: # semaphore作为异步上下文管理器，所以程序整体不会阻塞，只有当semaphore为零时，协程会挂起
            image = await get_flag(client, base_url, cc)
        async with semaphore: # 这两个使用semaphore的代码分开，是为了防止占用semaphore过久
            country = await get_country(client, base_url, cc)
    except httpx.HTTPStatusError as exc: # 错误处理
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        filename = country.replace(' ', '_') 
        await asyncio.to_thread(save_flag, image, f'{filename}.gif')
        status = DownloadStatus.OK
        msg = 'OK'
    
    if verbose and msg:
        print(cc, msg)
    return status