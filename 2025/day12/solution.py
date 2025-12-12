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

@timer_func
def part1(groups):
    areas = [g.count('#') for g in groups[:-1]]
    possible = 0
    for region in groups[-1].split('\n'):
        rl = region.split()
        l,w = map(int,rl[0][:-1].split('x'))
        counts = list(map(int,rl[1:]))
        if l*w >= sum([areas[i]*counts[i] for i in range(len(counts))]):
            possible += 1
    return possible

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            groups = [l.strip() for l in f.read().split('\n\n')]
            sol1 = part1(groups)
         
if __name__=='__main__':
    main()

