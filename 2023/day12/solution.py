import argparse
import time
from collections import deque
import heapq
import re

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

'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def place_windows(sizes, row):
    positions = {0: 1}
    for i, size in enumerate(sizes):
        new_positions = {}
        for k, v in positions.items():
            for n in range(k, len(row) - (sum(sizes[i:]) + len(sizes[i + 1:])-1)):
                if '.' not in row[n:n + size]:
                    if (i == len(sizes) - 1 and '#' not in row[n + size:]) or \
                       (i < len(sizes) - 1 and row[n + size] != '#'):
                        if n+size+1 not in new_positions:
                            new_positions[n+size+1] = 0
                        new_positions[n + size + 1] += v
                if row[n] == '#':
                    break
        positions = new_positions
    return sum(positions.values())

@timer_func
def part1( grid ):
    arrangements = 0
    for line in grid:
        row, nums = line.split()
        sizes = list(map(int, nums.split(',')))
        arrangements+=place_windows(sizes, row)
    return arrangements

@timer_func
def part2( grid ):
    arrangements = 0
    for line in grid:
        row, nums = line.split()
        sizes = list(map(int, nums.split(',')))
        row = '?'.join([row for i in range(5)])
        sizes = sizes*5
        arrangements+=place_windows(sizes, row)
    return arrangements

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = lines
            sol1 = part1(grid)
            sol2 = part2(grid)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

