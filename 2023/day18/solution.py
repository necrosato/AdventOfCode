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

timings = {}
def instrument(silent=False):
    def decorator(func):
        def wrap_func(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            duration = t2-t1
            if not silent:
                print(f'Function {func.__name__!r} executed in {(duration):.4f}s returned {result}')
            if func.__name__ not in timings:
                timings[func.__name__] = 0
            timings[func.__name__] += duration 
            return result
        return wrap_func
    return decorator

def vector_add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def setToGrid(lava):
    mini = min([l[0][0] for l in lava])
    maxi = max([l[0][0] for l in lava])
    minj = min([l[0][1] for l in lava])
    maxj = max([l[0][1] for l in lava])
    ioff = 0-mini
    joff = 0-minj
    grid = []
    print(maxi-mini+1, maxj-minj+1)
    for i in range(maxi-mini+1):
        grid.append([])
        print(i)
        for j in range(maxj-minj+1):
            grid[-1].append('.')
    for l in lava:
        grid[l[0][0]+ioff][l[0][1]+joff]= '#'
    return grid


def get_neighbors(grid, row, col):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for pair in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i = row+pair[0]
        j = col+pair[1]
        if 0 <= i < rows and 0 <= j < cols:
            if grid[i][j] != '#':
                neighbors.append((i,j,grid[i][j]))
    return neighbors

def flood(grid, start):
    perim = grid_find_all(grid, '#')
    inside = [start]
    while inside:
        i, j, v = inside.pop()
        grid[i][j] = '#'
        for neighbor in get_neighbors(grid, i, j):
            inside.append(neighbor)
    return grid

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                return (i, j, val)

def grid_find_all(grid, val):
    vals = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                vals.append((i, j, val))
    return vals

@timer_func
def part1( moves ):
    dirs = {'U':(-1,0),'D':(1,0),'R':(0,1),'L':(0,-1)}
    lava = set()
    pos = (0, 0)
    lava.add((pos, None))
    for direction, dist, color in moves:
        for i in range(dist):
            pos=vector_add(pos, dirs[direction])
            lava.add((pos, color))
    grid = setToGrid(lava)
    print('\n'.join([''.join(l) for l in grid]))
    i,j,v = grid_find(grid, '#')
    flood(grid, (i+1, j+1, '.'))
    print()
    print('\n'.join([''.join(l) for l in grid]))
    return sum([l.count('#') for l in grid])

@timer_func
def part2( moves ):
    dirs = {3:(-1,0),1:(1,0),0:(0,1),2:(0,-1)}
    lava = set()
    pos = (0, 0)
    lava.add((pos, None))
    for direction, dist, color in moves:
        direction = int(color[7])
        dist = int(color[2:6], 16)
        for i in range(dist):
            pos=vector_add(pos, dirs[direction])
            lava.add((pos, color))
    grid = setToGrid(lava)
    i,j,v = grid_find(grid, '#')
    flood(grid, (i+1, j+1, '.'))
    return sum([l.count('#') for l in grid])

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
            moves = [(l[0], int(l[1]), l[2]) for l in lines]
            sol1 = part1(moves)
            sol2 = part2(moves)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

