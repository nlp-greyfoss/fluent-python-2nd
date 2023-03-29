import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count  
from multiprocessing import queues 
from primes import is_prime, NUMBERS 

class PrimeResult(NamedTuple): 
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int] 
ResultQueue = queues.SimpleQueue[PrimeResult] 

def check(n: int) -> PrimeResult:
    t0 = perf_counter() 
    res = is_prime(n)
    return PrimeResult(n ,res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None: 
    """
    jobs保存了要检查的数字
    results用于保存结果
    """
    while n := jobs.get(): # 这里数字0作为worker完成工作的信号，如果不是0则继续循环
        results.put(check(n)) 
    results.put(PrimeResult(0, False, 0.0))  # 重新添加数字0告诉main loop工作完成了

def start_jobs(procs: int, jobs: JobQueue, results: ResultQueue) -> None: # procs 是要并行执行的进程数
    for n in NUMBERS:
        jobs.put(n) # 放入要检查的数字
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results)) # 为每个worker fork一个子进程
        proc.start() # 开启每个子进程
        jobs.put(0) # 为每个进程添加表示结束的0

def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])
    
    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()  # jobs和results都是队列
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)  # 开启进程来消耗jobs并产生results
    checked = report(procs, results)  # 检索并展示结果
    elapsed = perf_counter() - t0 
    print(f'{checked} checks in {elapsed:.2f}s') # 打印检查了多少数字和消耗的时间

def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs: # 循环知道所有的进程完成
        n, prime, elapsed = results.get() # 得到一个PrimeResult。调用.get()会阻塞直到队列中有元素
        if n == 0: # 如果为0，表面该进程结束了，增加进程完成的数量
            procs_done += 1
        else:
            checked += 1 # 否则，增加检查的数量
            label = "P" if prime else " "
            print(f'{n:16} {label} {elapsed:9.6f}s')
    return checked

if __name__ == '__main__':
    """
    $ python procs.py
    
    """
    main()