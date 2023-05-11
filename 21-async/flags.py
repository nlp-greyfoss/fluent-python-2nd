import time
from pathlib import Path
from typing import Callable

import httpx # 非标准库的引用一般位于标准库后面，并加上一个空行

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split() # 一些国家编码

BASE_URL = 'https://www.fluentpython.com/data/flags' # 国旗图片的位置
DEST_DIR = Path('downloaded') # 本地保存的路径


def save_flag(img: bytes, filename: str) -> None: # 保存图片字节到文件名
    (DEST_DIR / filename).write_bytes(img)
    
def get_flag(cc: str) -> bytes: # 基于给定的国家编码下载图片
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, follow_redirects=True) # 增加timeout是一个好的习惯；默认HTTPX不允许重定向
    resp.raise_for_status() # 如果HTTP状态码不是2XX，则抛出异常
    return resp.content

def download_many(cc_list: list[str]) -> int: # 这是核心函数，来与并发实现进行比较
    for cc in sorted(cc_list): 
        image = get_flag(cc)
        save_flag(image, f"{cc}.gif")
        print(cc, end=" ", flush=True) # end为 " "而不是换行，默认Python只显示包含换行的字符串，这里通过 flush让Python显示想要的字符
    
    return len(cc_list) 

def main(downloader: Callable[[list[str]], int]) -> None: 
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)