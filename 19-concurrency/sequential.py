from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class Result(NamedTuple): 
    prime: bool
    elapsed: float

def check(n: int) -> Result: 
    t0 = perf_counter()
    prime = is_prime(n)
    return Result(prime, perf_counter() -t0)

def main() -> None:
    print(f'Checking {len(NUMBERS)} numbers sequentially:')
    t0 = perf_counter()
    for n in NUMBERS:
        prime, elapsed = check(n)
        label = "P" if prime else " "
        print(f'{n:16} {label} {elapsed:9.6f}s')
    
    elapsed = perf_counter() - t0 # 计算总共花费的时间
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    """
    $ python sequential.py 
    Checking 20 numbers sequentially:
               2 P  0.000001s
 142702110479723 P  0.569349s
 299593572317531 P  1.002950s
3333333333333301 P  3.006190s
3333333333333333    0.000010s
3333335652092209    2.710673s
4444444444444423 P  3.282786s
4444444444444444    0.000002s
4444444488888889    3.148743s
5555553133149889    3.864314s
5555555555555503 P  3.617900s
5555555555555555    0.000011s
6666666666666666    0.000001s
6666666666666719 P  4.102377s
6666667141414921    3.877022s
7777777536340681    4.221931s
7777777777777753 P  4.531805s
7777777777777777    0.000010s
9999999999999917 P  4.787778s
9999999999999999    0.000010s
Total time: 42.73s

    """
    main()