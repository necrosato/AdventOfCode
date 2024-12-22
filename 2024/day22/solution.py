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

def evolve(n, m=16777216):
    s1 = (n^(n*64))%m
    s2 = (s1^(s1//32))%m
    s3 = (s2^(s2*2048))%m
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
    totals = {}
    for i in ints:
        n = i
        seen = set()
        track = []
        for c in range(2000):
            track.append(evolve(n))
            n = track[-1][0]
            seq = tuple(t[2] for t in track[-4:])
            if c >= 3 and seq not in seen:
                if seq not in totals:
                    totals[seq] = 0
                totals[seq]+=track[-1][1]
                seen.add(seq)
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

