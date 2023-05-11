from concurrent import futures

from flags import save_flag, get_flag, main # 重用一些函数


def download_one(cc: str): # 下载单个图像，这可作为每个worker的task
    image = get_flag(cc)
    save_flag(image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    
    with futures.ThreadPoolExecutor(max_workers=3) as executor: 
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc) # 安排一个待执行的callable，返回一个future对象
            to_do.append(future)
            print(f"Scheduled for {cc}: {future}")
        
        for count, future in enumerate(futures.as_completed(to_do), 1): #  as_completed yields 完成状态的 future
            res: str = future.result() # 得到future的状态
            print(f'{future} result: {res!r}')
    
    return count 

if __name__ == '__main__':
    main(download_many)