import argparse
import time
from collections import deque
import heapq

'''
some generic helper functions
'''
timings = {}
def timer_func(silent=False):
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

def get_neighbors(grid, row, col):
    neighbors = 0
    rows, cols = len(grid), len(grid[0])
    for pair in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i = row+pair[0]
        j = col+pair[1]
        if 0 <= i < rows and 0 <= j < cols:
            neighbors += grid[i][j]
    return neighbors

'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def get_quadrant(x, y, width, height):
    """Gets the quadrant of a point given its x and y coordinates."""
    xax = width//2
    yax = height//2
    if x > xax and y > yax:
        return 1
    elif x < xax and y > yax:
        return 2
    elif x < xax and y < yax:
        return 3
    elif x > xax and y < yax:
        return 4
    else:
        return None  # Point lies on an axis

@timer_func()
def part1( robots ):
    bathroom = (101, 103)    
    steps = 100
    tiles = {}
    for p,v in robots:
        fp = ((p[0]+(v[0]*steps))%bathroom[0], (p[1]+(v[1]*steps))%bathroom[1])
        if fp not in tiles: 
            tiles[fp] = 0
        tiles[fp]+=1
    quadrants = {1:0, 2:0, 3:0, 4:0}
    for tile in tiles:
        quadrant = get_quadrant(*tile, *bathroom)
        if quadrant:
            quadrants[quadrant] += tiles[tile]
    safety_factor = 1
    for quadrant in quadrants:
        safety_factor *= quadrants[quadrant]
    return safety_factor

def score(tiles):
    score = 0
    width = len(tiles)
    height = len(tiles[0])
    for i in range(width):
        for j in range(height):
            if tiles[i][j] > 0:
                score += get_neighbors(tiles, i, j)
    return score 

@timer_func()
def part2( robots ):
    bathroom = (101, 103)    
    steps = 0
    max_score = 0
    max_score_steps = 0
    tiles = [[0]*bathroom[0] for i in range(bathroom[1])]
    for p,v in robots:
        tiles[p[1]][p[0]] += 1
    for steps in range(1, 101*103):
        ng = []
        for p,v in robots:
            fp = ((p[0]+v[0]+bathroom[0])%bathroom[0], (p[1]+v[1]+bathroom[1])%bathroom[1])
            ng.append((fp, v))
            tiles[p[1]][p[0]] -= 1
            tiles[fp[1]][fp[0]] += 1
        robots = ng
        ns = score(tiles)
        if ns > max_score:
            max_score = ns
            max_score_steps = steps
            for line in tiles:
                print(''.join(list(map(str,line))).replace('0','.'))
            print('found new max {} at {}'.format(ns, steps))
    return max_score_steps

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            lines = [line.split() for line in lines]
            robots = [(tuple(map(int,line[0][2:].split(','))), tuple(map(int,line[1][2:].split(',')))) for line in lines]
            sol1 = part1(robots)
            sol2 = part2(robots)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
        
if __name__=='__main__':
    main()

