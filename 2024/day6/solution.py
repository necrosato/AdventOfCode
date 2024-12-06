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

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == val:
                return (i, j, val)
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
@timer_func
def part1( grid ):
    start = grid_find(grid, '^')
    pos = grid_find(grid, '^')
    di = 0
    seen = set()
    returned = False
    while not returned:
        d = dirs[di%4]
        ni = pos[0]+d[0]
        nj = pos[1]+d[1]
        seen.add((pos[0], pos[1]))
        if ni in range(len(grid)) and nj in range(len(grid[ni])):
            if grid[ni][nj] != '#':
                pos = (ni, nj)
            else:
                di+=1
        else:
            returned = True
    return len(seen)

@timer_func
def part2( grid ):
    start = grid_find(grid, '^')
    loopers = 0
    li = len(grid)
    lj = len(grid[0])

    pos = grid_find(grid, '^')
    di = 0
    original_seen = set()
    returned = False
    while not returned:
        d = dirs[di%4]
        ni = pos[0]+d[0]
        nj = pos[1]+d[1]
        original_seen.add((pos[0], pos[1]))
        if ni < li and ni > -1 and nj < lj and nj > -1:
            if grid[ni][nj] != '#':
                pos = (ni, nj)
            else:
                di+=1
        else:
            returned = True

    for i in range(li):
        for j in range(lj):
            if (i, j) != (start[0], start[1]) and (i, j) in original_seen:
                returned = False
                grid[i][j] = '#'
                seen = set()
                di = 0
                pos = grid_find(grid, '^')
                seen.add((pos[0], pos[1], d))
                while not returned:
                    d = dirs[di%4]
                    ni = pos[0]+d[0]
                    nj = pos[1]+d[1]
                    new = (ni, nj, d)
                    if new in seen:
                        returned = True
                        loopers += 1
                    else:
                        seen.add(new)
                        if ni < li and ni > -1 and nj < lj and nj > -1:
                            if grid[ni][nj] != '#':
                                pos = new
                            else:
                                di+=1
                        else:
                            returned = True
                grid[i][j] = '.' 
    return loopers

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = [list(line) for line in lines]
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

