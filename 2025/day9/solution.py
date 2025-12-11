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

def print_area(area):
    for l in area:
        print(''.join(l))
    print()


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

def int_grid(lines):
    return [list(map(int, line.split())) for line in lines]

def coordinate_list(grid):
    return [(i, j, grid[i][j]) for i in range(len(grid)) for j in range(len(grid[i]))]
 
def transpose(grid):
    return list(map(list, zip(*grid)))

def get_neighbors(x,y):
    return[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

@timer_func
def part1( grid ):
    pairs = []
    for l1 in grid:
        for l2 in grid:
            pairs.append((l1,l2))
    areas = []
    for p1,p2 in pairs:
        areas.append((abs(p2[0]-p1[0])+1)*(abs(p2[1]-p1[1])+1))
    return(max(areas))

@timer_func
def part2( grid ):
    minx = min([p[0] for p in grid])
    maxx = max([p[0] for p in grid])
    miny = min([p[1] for p in grid])
    maxy = max([p[1] for p in grid])
    xd = maxx-minx+1
    xy = maxy-miny+1
    '''
    area = []
    print('here')
    for i in range(xy):
        l = []
        for _ in range(xd):
            l.append('.')
        area.append(l)
        print(i,xy)
    '''
    reds = set()
    greens = set()
    last = None
    for j,i in grid:
        reds.add((j,i))
        if last:
            di = 1 if last[1] > i else -1
            dj = 1 if last[0] > j else -1
            for ni in range(i,last[1]+di,di):
                for nj in range(j,last[0]+dj,dj):
                    greens.add((nj,ni))
        last = (j,i)
    di = 1 if last[1] > i else -1
    dj = 1 if last[0] > j else -1
    for ni in range(i,last[1]+di,di):
        for nj in range(j,last[0]+dj,dj):
            greens.add((nj,ni))
    
    fsx = 97850
    fsy = 51415
    targets = [(fsx,fsy)]
    while targets:
        target = targets.pop()
        greens.add(target)
        neighbors = get_neighbors(*target)
        for neighbor in neighbors:
            if neighbor not in greens and neighbor not in reds:
                targets.append(neighbor)
        print(len(targets),len(greens))
    '''
    for x,y in grid:
        j = x-minx
        i = y-miny
        area[i][j] = '#'
        if last:
            di = 1 if last[1] > i else -1
            dj = 1 if last[0] > j else -1
            for ni in range(i,last[1]+di,di):
                for nj in range(j,last[0]+dj,dj):
                    if area[ni][nj] == '.':
                        area[ni][nj] = 'O'
        last = (j,i)
    j = grid[0][0] - minx
    i = grid[0][1] - miny
    di = 1 if last[1] > i else -1
    dj = 1 if last[0] > j else -1
    for ni in range(i,last[1]+di,di):
        for nj in range(j,last[0]+dj,dj):
            if area[ni][nj] == '.':
                area[ni][nj] = 'O'
    #print_area(area)
    '''

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [tuple(map(int,l.strip().split(','))) for l in f.readlines()]
            sol1 = part1(grid)
            sol2 = part2(grid)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

