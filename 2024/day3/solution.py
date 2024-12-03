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
    total = 0
    for line in grid:
        if 'mul' in line:
            n1,n2=list(map(int,line[4:-1].split(',')))
            total+=n1*n2
    return total

@timer_func
def part2( grid ):
    total = 0
    enabled = True
    for line in grid:
        if line == 'do()':
            enabled = True
        elif line == 'don\'t()':
            enabled = False
        else:
            if enabled:
                n1,n2=list(map(int,line[4:-1].split(',')))
                total+=(n1*n2)
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            pattern = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
            new_lines = []
            for line in lines:
                new_lines += list(pattern.findall(line))
            sol1 = part1(new_lines)
            sol2 = part2(new_lines)
        
if __name__=='__main__':
    main()

