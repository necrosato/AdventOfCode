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
    windows = {}
    free_windows = {}
    mem = ['.'] * sum(nums)
    i = 0
    for n in range(len(nums)):
        free = n%2 != 0
        num = nums[n]
        if not free:
            mem[i:i+num] = [n//2]*num
            windows[n//2] = (i, i+num)
        else:
            if num not in free_windows:
                free_windows[num] = []
            free_windows[num].append((i, i+num))
        i += num
    return (len(nums)-1)//2, mem, windows, free_windows

@timer_func
def part1( grid ):
    f, mem, windows, free_windows = build_mem(grid)
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

def find_free(windows, n):
    slot = None
    for i in range(n, 10):
        if i in windows and len(windows[i]) > 0:
            if slot is None or slot[0] > windows[i][0][0]:
                slot = windows[i][0]
    if slot:
        windows[slot[1]-slot[0]].pop(0)
    return slot

@timer_func
def part2( grid ):
    f, mem, windows, free_windows = build_mem(grid)
    for i in range(f,-1,-1):
        nc = windows[i] 
        fc = find_free(free_windows, nc[1]-nc[0])
        if fc and fc[1] <= nc[0]:
            mem[fc[0]:fc[0]+(nc[1]-nc[0])] = mem[nc[0]:nc[1]]
            mem[nc[0]:nc[1]] = ['.'] * (nc[1]-nc[0])
            nf = (fc[0]+(nc[1]-nc[0]), fc[1])
            nfl = nf[1]-nf[0]
            if nfl > 0:
                if nfl not in free_windows:
                    free_windows[nfl] = []
                free_windows[nfl].append(nf)
                free_windows[nfl] = sorted(free_windows[nfl])
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

