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

def int_grid(lines):
    return [list(map(int, line.split())) for line in lines]
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def expand(stone, blink, blinks, memo):
    stone_count = 1
    if blink == blinks:
        memo[(stone, blink)] = stone_count
        return 1
    if (stone, blink) in memo:
        return memo[(stone, blink)]
    if stone == 0:
        stone_count = expand(1, blink + 1, blinks, memo)
    elif len(str(stone))%2==0:
        first = int(str(stone)[0:len(str(stone))//2])
        second = int(str(stone)[len(str(stone))//2:])
        stone_count = (expand(first, blink + 1, blinks, memo) + expand(second, blink + 1, blinks, memo))
    else:
        stone_count = expand(stone * 2024, blink + 1, blinks, memo)
    memo[(stone, blink)] = stone_count
    return stone_count


@timer_func
def part1( grid ):
    line = grid[0]
    memo = {}
    total = 0
    for stone in line:
        total += expand(stone, 0, 25, memo)
    return total

@timer_func
def part2( grid ):
    line = grid[0]
    memo = {}
    total = 0
    for stone in line:
        total += expand(stone, 0, 75, memo)
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = int_grid(lines)
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

