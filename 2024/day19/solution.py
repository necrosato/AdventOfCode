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

memo = {}
def can_make(design, available):
    if design == '':
        return 1
    if design not in memo:
        memo[design] = 0
        for pattern in available:
            if design[:len(pattern)] == pattern:
                memo[design] += can_make(design[len(pattern):], available)
    return memo[design]

@timer_func
def part1( available, designs ):
    return sum([can_make(design, available)>0 for design in designs])

@timer_func
def part2( available, designs ):
    return sum([can_make(design, available) for design in designs])

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            available = lines[0].split(', ')
            designs = lines[2:]
            sol1 = part1(available, designs)
            sol2 = part2(available, designs)
         
if __name__=='__main__':
    main()
