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

def build_mem(grid):
    nums = list(map(int,list(grid[0])))
    files = [nums[i] for i in range(0, len(nums), 2)]
    frees = [nums[i] for i in range(1, len(nums), 2)]
    mem = ['.'] * sum(nums)
    i = 0
    f = 0
    free = False
    for num in nums:
        if not free:
            mem[i:i+num] = [f]*num
            f += 1
        i += num
        free = not free 
    return f, mem

@timer_func
def part1( grid ):
    f, mem = build_mem(grid)
    start = 0
    end = len(mem)-1
    while end-start > 1: 
        while mem[start] != '.' and start < end:
            start += 1
        while mem[end] == '.' and start < end:
            end -= 1
        if (end-start) > 1:
            mem[start] = mem[end]
            mem[end] = '.'
    return checksum(mem)


def find_free(mem, n):
    free_start = 0
    in_free = False
    for i in range(0, len(mem)):
        if mem[i] == '.':
            if not in_free:
                in_free = True
                free_start = i
        elif in_free:
            if i-free_start >= n:
                return (free_start, i)
            in_free = False
        else:
            in_free = False
    return None

def find_num(mem, n):
    n_start = 0
    in_n = False
    for i in range(len(mem)):
        if mem[i] == n:
            if not in_n:
                in_n = True
                n_start = i
        elif in_n:
            return (n_start, i)
        else:
            in_n = False
    if in_n:
        return (n_start, i+1)
    return None

@timer_func
def part2( grid ):
    f, mem = build_mem(grid)
    for i in range(f-1,-1,-1):
        nc = find_num(mem, i)
        fc = find_free(mem, nc[1]-nc[0])
        if fc and fc[1] <= nc[0]:
            mem[fc[0]:fc[0]+(nc[1]-nc[0])] = mem[nc[0]:nc[1]]
            mem[nc[0]:nc[1]] = ['.'] * (nc[1]-nc[0])
    return checksum(mem)

def checksum(mem):
    checksum = 0
    for i in range(len(mem)):
        checksum += 0 if mem[i] == '.' else i*mem[i]
    return checksum

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = lines
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

