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

def antinodes(grid, start, length):
    points = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            v = grid[i][j]
            if v != '.':
                if v not in points:
                    points[v] = []
                points[v].append((i, j))
    antinodes = set()
    for c in points:
        coords = points[c]
        for i in range(len(coords)):
            for j in range(i+1,len(coords)):
                slope = (coords[j][0] - coords[i][0], coords[j][1]-coords[i][1])
                for k in range(start,start+length):
                    antinodes.add((coords[i][0]-(k*slope[0]),coords[i][1]-(k*slope[1])))
                    antinodes.add((coords[j][0]+(k*slope[0]),coords[j][1]+(k*slope[1])))
    total = 0
    for a in antinodes:
        if a[0] > -1 and a[0] < len(grid) and a[1] > -1 and a[1] < len(grid[0]):
            total += 1
    return total

@timer_func
def part1( grid ):
    return antinodes(grid, 1, 1)

@timer_func
def part2( grid ):
    return antinodes(grid, 0, len(grid))

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
