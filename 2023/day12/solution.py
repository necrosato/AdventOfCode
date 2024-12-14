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

def find_all(line, val):
    vals = []
    for i in range(len(line)):
        if line[i] == val:
            vals.append(i)
    return vals
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

pattern = re.compile(r'#+')
def check_buf(buf, sizes):
    springs = re.findall(pattern,''.join(buf))
    return list(map(len,springs)) == sizes

@timer_func
def part1( grid ):
    arrangements = 0
    for line in grid:
        la = 0
        row, nums = line.split()
        sizes = list(map(int, nums.split(',')))
        qs = find_all(row, '?')
        buf = list(row)
        for q in range(2**len(qs)):
            qb = bin(q)[2:].zfill(len(qs))
            assert(len(qb) == len(qs))
            for i in range(len(qb)):
                buf[qs[i]] = '.' if qb[i] == '0' else '#'
            la += check_buf(buf, sizes)
        arrangements+=la
        '''
        windows = []
        window_start = 0
        for size in sizes:
            windows.append([window_start,window_start+size, size])
            window_start += size+1
        for i in reversed(range(len(windows))):
            window = windows[i]
            while window[1] < len(row)-1:
                i==len(windows)-1 or windows[i+1][0]-window[1]
                if window[1] < len(row)-2 and
                window[0] += 1
                window[1] += 1
            while  and windows[i][1]
        for word in words:
            if sizes[i] == len(word):
                pass    
            else:
                qs = word.count('?')
            i+=1
        assert(i == len(sizes))
        '''
 
    return arrangements

@timer_func
def part2( grid ):
    pass

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

