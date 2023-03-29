
import asyncio
import itertools
import time
from primes import is_prime

async def spin(msg: str) -> None: 
    """
    不再需要Event参数
    """
    for char in itertools.cycle(r"\|/-"): # itertools.cycle一次yield出一个字符，这是一个无限循环
        status = f"\r{char} {msg}" # text-mode的动画技巧： 移将光标移回带有回车ASCII控制字符（'\r'）的行首
        print(status, end="", flush=True)
        try:
            await asyncio.sleep(.1) # 使用asyncio.sleep(.1)而不是time.sleep(.1)来暂停，但不会阻塞其他协程
        except asyncio.CancelledError:  #  当cancel方法被调用时会抛出该异常
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="") # 通过空格重写清 空状态行，并将光标移回开始处

async def slow() -> int:
    #await asyncio.sleep(3) # 同样也使用了asyncio.sleep
    # time.sleep(3) 不会出现动画 因为它会阻塞主线程——唯一的线程，本脚本的代码任意时间内仅有一个协程在执行。 在这个 sleep返回后，spinner任务被取消，控制流从未进入spin协程内。
    return is_prime(5_000_111_000_222_021)





def main() -> None: # main是唯一的普通方法，其他的都是协程
    result = asyncio.run(supervisor()) # 开启event.loop，main函数会阻塞直到supervisor()方法返回，supervisor的返回值会作为asyncio.run的返回值
    print(f"Answer: {result}")

async def supervisor() -> int: # 通过 async def 定义协程
    spinner = asyncio.create_task(spin("thinking!")) # 安排spin的执行，它会立马返回一个asyncio.Task实例

    print(f"spinner object: {spinner}") # 输出类似 <Task pending name='Task-2' coro=<spin() running at /path/to/spinner_async.py:11>>
    result = await slow() # await 关键字调用slow()，阻塞supervisor，直到slow返回，返回值会赋给result
    spinner.cancel() # 抛出一个CancelledError异常
    return result

if __name__ == '__main__':
    main()