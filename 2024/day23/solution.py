import argparse
import time
from collections import deque
import heapq
import itertools

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

def triangles(connections, source):
    res = set()
    for inter in connections[source]:
        for dest in connections[inter]:
            if dest in connections[source]:
                res.add(tuple(sorted([source, inter, dest])))
    return res

@timer_func
def part1( connections ):
    loops = set()
    for source in connections:
        loops |= triangles(connections, source)
    hast = 0
    for loop in loops:
        tloop = False
        for c in loop:
            tloop |= 't' == c[0]
        hast += tloop
    return hast

cm = {}
def check(connections, lan):
    key = lan
    if key in cm:
        return cm[key]
    for c in lan:
        if not set(lan).issubset(connections[c]):
            cm[key] = False
            return False
    cm[key] = True
    return True

def biggest_lan(connections):
    sparse_lans = [tuple(sorted(lan)) for lan in connections.values()]
    lans = set()
    for lan in sparse_lans:
        found = False
        for i in reversed(range(len(lan))):
            for comb in itertools.combinations(lan, i+1):
                if check(connections, comb):
                    lans.add(comb)
                    found = True
            if found:
                break
    return ','.join(sorted(sorted(lans, key=lambda x:len(x))[-1]))

@timer_func
def part2( connections ):
    for comp in connections:
        connections[comp].add(comp)
    return biggest_lan(connections)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip().split('-') for l in f.readlines()]
            connections = {}
            for s,d in lines:
                if s not in connections:
                    connections[s] = set()
                connections[s].add(d)
                if d not in connections:
                    connections[d] = set()
                connections[d].add(s)
            sol1 = part1(connections)
            sol2 = part2(connections)
         
if __name__=='__main__':
    main()

