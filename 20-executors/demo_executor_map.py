from time import sleep, strftime 
from concurrent import futures

def display(*args): # 简单地打印了它的参数
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n): 
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n)) # 当它执行时打印一条信息
    sleep(n) 
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n)) # 结束时也打印一条信息
    return n * 10 # 

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  
    results = executor.map(loiter, range(5))  
    display('results:', results)  
    display('Waiting for individual results:') 
    for i, result in enumerate(results): # 实际上调用的是_f.result()，该方法会阻塞直到future完成
        display(f'result {i}: {result}')

if __name__ == '__main__':
    main()