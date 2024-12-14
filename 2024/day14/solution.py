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

def get_neighbors(grid, row, col, range_val=1, diagonals=False):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for i in range(row - range_val, row + range_val + 1):
        for j in range(col - range_val, col + range_val + 1):
            if 0 <= i < rows and 0 <= j < cols and (i != row or j != col):
                if diagonals or i == row or j == col:
                    neighbors.append(grid[i][j])
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

@timer_func
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

def score(robots, bathroom):
    tiles = [[0]*bathroom[0] for i in range(bathroom[1])]
    score = 0
    for p,v in robots:
        tiles[p[1]][p[0]] += 1
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] > 0:
                score += sum(get_neighbors(tiles, i, j, diagonals=False))
    return score 

def print_bathroom(robots, bathroom):
    tiles = [[0]*bathroom[0] for i in range(bathroom[1])]
    for p,v in robots:
        tiles[p[1]][p[0]] += 1
    for line in tiles:
        print(''.join(list(map(str,line))).replace('0','.'))

@timer_func
def part2( robots ):
    bathroom = (101, 103)    
    steps = 0
    max_score = 0
    max_score_steps = 0
    for steps in range(1, 101*103):
        ng = []
        for p,v in robots:
            fp = ((p[0]+v[0]+bathroom[0])%bathroom[0], (p[1]+v[1]+bathroom[1])%bathroom[1])
            ng.append((fp, v))
        robots = ng
        ns = score(robots, bathroom)
        if ns > max_score:
            max_score = ns
            max_score_steps = steps
            print_bathroom(robots, bathroom)
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
        
if __name__=='__main__':
    main()

