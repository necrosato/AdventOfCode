import argparse
import time
import functools

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


@functools.lru_cache()
def paths_from(start,end):
    if start == end:
        return 1
    return sum([paths_from(n,end) for n in graph[start]])

@timer_func
def part1( grid ):
    return paths_from('svr','out')

@timer_func
def part2( grid ):
    return paths_from('svr','fft')*paths_from('fft','dac')*paths_from('dac','out')

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
            global graph
            graph = { line[0][:-1]:line[1:] for line in lines }
            part1(lines)
            part2(lines)
         
if __name__=='__main__':
    main()

