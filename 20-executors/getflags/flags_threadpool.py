from concurrent import futures

from flags import save_flag, get_flag, main # 重用一些函数


def download_one(cc: str): # 下载单个图像，这可作为每个worker的task
    image = get_flag(cc)
    save_flag(image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor: # 通过上下文管理器来实例化ThreadPoolExecutor，在__exit__方法会调用executor.shutdown(wait=True)
        es = executor.map(download_one, sorted(cc_list)) # 它返回一个生成器，可以迭代来检索每个函数调用返回的值——在这种情况下，每个download_one将返回一个国家编码
    
    return len(cc_list) 

if __name__ == '__main__':
    main(download_many)