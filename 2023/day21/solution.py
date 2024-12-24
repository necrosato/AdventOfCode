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

def get_neighbors(grid, row, col, infinite=False):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for pair in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i = row+pair[0]
        j = col+pair[1]
        if ((0 <= i < rows and 0 <= j < cols) or infinite) and grid[i%len(grid)][j%len(grid[0])]!='#':
            neighbors.append((i,j,grid[i%len(grid)][j%len(grid[0])]))
    return neighbors
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                return (i, j, val)

@timer_func
def part1( grid ):
    steps = 64
    positions = set([grid_find(grid, 'S')])
    for s in range(steps):
        next_positions = set()
        for position in positions:
            next_positions |= set(get_neighbors(grid, position[0], position[1]))
        positions = next_positions
    return len(positions)

@timer_func
def part2( grid ):
    steps = 100
    positions = set([grid_find(grid, 'S')])
    for s in range(steps):
        next_positions = set()
        for position in positions:
            next_positions |= set(get_neighbors(grid, position[0], position[1], True))
        positions = next_positions
    return len(positions)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [list(l.strip()) for l in f.readlines()]
            sol1 = part1(grid)
            sol2 = part2(grid)
         
if __name__=='__main__':
    main()

