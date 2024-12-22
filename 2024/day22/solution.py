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

def prune(n, m=16777216):
    return n%m
def evolve(n):
    s1 = prune(n^(n*64))
    s2 = prune(s1^(s1//32))
    s3 = prune(s2^(s2*2048))
    return (s3, s3%10, (s3%10)-(n%10))

@timer_func
def part1( ints ):
    total = 0
    for i in ints:
        n = i
        for c in range(2000):
            n,price,diff=evolve(n)
        total += n
    return total

@timer_func
def part2( ints ):
    total = 0
    totals = {}
    for i in ints:
        seen = set()
        n = i
        track = []
        for c in range(2000):
            track.append(evolve(n))
            seq = tuple(t[2] for t in track[-4:])
            if c >= 3 and seq not in seen:
                if seq not in totals:
                    totals[seq] = 0
                totals[seq]+=track[-1][1]
                seen.add(seq)
            n = track[-1][0]
    return max(totals.values())

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [int(l.strip()) for l in f.readlines()]
            sol1 = part1(lines)
            sol2 = part2(lines)
         
if __name__=='__main__':
    main()

