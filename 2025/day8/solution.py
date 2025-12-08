import argparse
import time
from collections import deque
import heapq
import math

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

def dists(grid):
    ds = {}
    for l1 in grid:
        for l2 in grid:
            d = math.dist(l1,l2)
            if l1 != l2:
                if d not in ds:
                    ds[d] = []
                ds[d].append((l1,l2))
    return ds
 
@timer_func
def part1( grid ):
    circuits = list(map(set,[[l] for l in grid]))
    connections = {}
    ds = dists(grid)
    i = 0
    for d in sorted(ds):
        for l1,l2 in ds[d]:
            if (l1 not in connections or l2 not in connections) or (l1 not in connections[l2] and l2 not in connections[l1]):
                if l1 not in connections:
                    connections[l1] = set()
                if l2 not in connections:
                    connections[l2] = set()
                connections[l1].add(l2)
                connections[l2].add(l1)

                circuit = set([l1,l2])
                tmp = [circuit]
                for c in circuits:
                    if l1 in c or l2 in c:
                        circuit.update(c)
                    else:
                        tmp.append(c)
                circuits = tmp
                i += 1
            if i == len(grid):
                lengths = list(sorted(list(map(len,circuits))))[-3:]
                return lengths[0]*lengths[1]*lengths[2]

@timer_func
def part2( grid ):
    circuits = list(map(set,[[l] for l in grid]))
    connections = {}
    ds = dists(grid)
    for d in sorted(ds):
        for l1,l2 in ds[d]:
            if (l1 not in connections or l2 not in connections) or (l1 not in connections[l2] and l2 not in connections[l1]):
                if l1 not in connections:
                    connections[l1] = set()
                if l2 not in connections:
                    connections[l2] = set()
                connections[l1].add(l2)
                connections[l2].add(l1)

                circuit = set([l1,l2])
                tmp = [circuit]
                for c in circuits:
                    if l1 in c or l2 in c:
                        circuit.update(c)
                    else:
                        tmp.append(c)
                circuits = tmp
            if len(circuits) == 1:
                return l1[0]*l2[0]

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

