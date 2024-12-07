import argparse
import time
from collections import deque
import heapq

'''
some generic helper functions
'''
def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s returned {result}')
        return result
    return wrap_func
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def results(parts):
    results = set()
    slots = len(parts)-1
    maxbin = '1' * slots if slots > 0 else '0'
    for i in range(int(maxbin, 2)+1):
        temp = parts[0]
        ibs = bin(i)[2:].zfill(slots)
        for pi in range(slots): 
            if ibs[pi] == '0':
                temp += parts[pi+1]
            else:
                temp *= parts[pi+1]
        results.add(temp)
    return results

@timer_func
def part1( grid ):
    total = 0
    for line in grid:
        res = line[0]
        parts = line[1:]
        if res in results(parts):
            total += res
    return total 
    
def concat_results(parts):
    all_results = set()
    for sep in range(len(parts)-1):
        lhs = parts[0:sep+1]
        rhs = parts[sep+1:]
        for lr in results(lhs):
            concat = [int(str(lr)+str(rhs[0]))] + rhs[1:]
            all_results |= concat_results(concat) | results(concat)
    return all_results

@timer_func
def part2( grid ):
    total = 0
    for line in grid:
        res = line[0]
        parts = line[1:]
        if res in results(parts) or res in concat_results(parts):
            total += res
    return total 

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
            grid = [[int(line[0][:-1])] + list(map(int, line[1:])) for line in lines]
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

