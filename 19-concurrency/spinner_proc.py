import itertools
import time
from multiprocessing import Process, Event
from multiprocessing import synchronize
from primes import is_prime

def spin(msg: str, done: Event) -> None: 
    """
    该函数运行在另一个线程。done参数是一个threading.Event的实例，一个简单的同步线程的对象。
    """
    for char in itertools.cycle(r"\|/-"): # itertools.cycle一次yield出一个字符，这是一个无限循环
        status = f"\r{char} {msg}" # text-mode的动画技巧： 移将光标移回带有回车ASCII控制字符（'\r'）的行首
        print(status, end="", flush=True)
        if done.wait(.1): # 当event被另一线程设置过，该方法返回True；如果timeout后，返回False
            break # 退出无限循环
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="") # 通过空格重写清 空状态行，并将光标移回开始处

def supervisor() -> int:
    done = Event()

    spinner = Process(target=spin, args=("thinking!", done)) # 用法类似Thread
    print(f"spinner object: {spinner}") # 打印如  <Process name='Process-1' parent=14868 initial>，其中14868是运行本脚本的进程ID
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

def slow() -> int:
    """该函数由主线程调用。调用sleep会阻塞主线程，但GIL被释放，因此spinner线程可以接着运行"""
    # time.sleep(3) # 
    return is_prime(5_000_111_000_222_021)

def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")

if __name__ == '__main__':
    main()