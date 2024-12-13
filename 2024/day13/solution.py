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

def determinant(u,v):
    return u[0]*v[1]-u[1]*v[0]

def solve(u1,u2,v):
    d,n1,n2=determinant(u1,u2),determinant(v,u2),determinant(u1,v)
    if n1%d==0 and n2%d==0:
        return (n1//d, n2//d)
    return None

def cost(buttons):
    if buttons:
        return 3*buttons[0]+buttons[1]
    return 0

@timer_func
def part1( grid ):
    total = 0
    for a, b, p in grid:
        total += cost(solve(a,b,p))
    return total

@timer_func
def part2( grid ):
    offset = 10000000000000
    total = 0
    for a, b, p in grid:
        op = (p[0]+offset, p[1]+offset)
        total += cost(solve(a,b,op))
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            chunks = [l.strip() for l in f.read().split('\n\n')]
            np = re.compile(r'\d+')
            grid = []
            for chunk in chunks:
                a,b,p = [line.strip() for line in chunk.split('\n')]
                a = tuple(map(int,re.findall(np, a)))
                b = tuple(map(int,re.findall(np, b)))
                p = tuple(map(int,re.findall(np, p)))
                grid.append([a, b, p])
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

