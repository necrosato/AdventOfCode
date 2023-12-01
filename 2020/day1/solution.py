import argparse
import time

def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s returned {result}')
        return result
    return wrap_func

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def findSumPair(nums, sumTo):
    seen = set()
    for n in nums:
        c = sumTo - n
        if c in seen:
            return c,n
        seen.add(n)

@timer_func
def part1( nums ):
    x,y = findSumPair(nums, 2020)
    return x*y 

@timer_func
def part2( nums ):
    for n in nums:
        c = 2020 - n
        p = findSumPair(nums, c)
        if p:
            return p[0]*p[1]*n

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            nums = [int(l) for l in lines]
            sol1 = part1(nums)
            sol2 = part2(nums)
        
if __name__=='__main__':
    main()

