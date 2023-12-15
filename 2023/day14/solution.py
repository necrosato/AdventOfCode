import argparse
import time
from copy import deepcopy

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

def move_down(grid):
    for r in range(len(grid)-1, -1, -1):
        for c in range(len(grid[r])):
            if grid[r][c] == 'O':
                for i in range(r+1, len(grid), 1):
                    if grid[i][c] != '.':
                        break
                    grid[i][c] = grid[i-1][c]
                    grid[i-1][c] = '.'

def move_up(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'O':
                for i in range(r-1, -1, -1):
                    if grid[i][c] != '.':
                        break
                    grid[i][c] = grid[i+1][c]
                    grid[i+1][c] = '.'

def move_left(grid):
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if grid[r][c] == 'O':
                for i in range(c-1, -1, -1):
                    if grid[r][i] != '.':
                        break
                    grid[r][i] = grid[r][i+1]
                    grid[r][i+1] = '.'

def move_right(grid):
    for c in range(len(grid[0])-1, -1, -1):
        for r in range(len(grid)):
            if grid[r][c] == 'O':
                for i in range(c+1, len(grid[0]), 1):
                    if grid[r][i] != '.':
                        break
                    grid[r][i] = grid[r][i-1]
                    grid[r][i-1] = '.'

def sum_load(grid):
    return sum([grid[r].count('O') * (len(grid)-r) for r in range(len(grid))])

@timer_func
def part1( grid ):
    move_up(grid)
    return sum_load(grid)

@timer_func
def part2( grid ):
    seen = {}
    i = 0
    while '\n'.join([''.join(r) for r in grid]) not in seen:
        seen['\n'.join([''.join(r) for r in grid])] = i
        i+=1
        for f in [move_up, move_left, move_down, move_right]:
            f(grid)
    cycle_start = seen['\n'.join([''.join(r) for r in grid])]
    cycle_len = i - cycle_start
    di = cycle_start + ((1000000000 - cycle_start) % cycle_len)
    return sum_load([list(l) for l in {v:k for k,v in seen.items()}[di].split('\n')])

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [list(l.strip()) for l in f.readlines()]
            part1(deepcopy(grid))
            part2(deepcopy(grid))
        
if __name__=='__main__':
    main()

