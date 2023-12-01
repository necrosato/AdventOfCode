import argparse
import time

def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s returned {result}')
        return result
    return wrap_func

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

@timer_func
def part1( grid ):
    passed = 0
    for l in grid:
        count = l[2].count(l[1])
        if count >= int(l[0][0]) and count <= int(l[0][1]):
            passed += 1
    return passed

@timer_func
def part2( grid ):
    passed = 0
    for l in grid:
        c0 = l[2][int(l[0][0])-1]
        c1 = l[2][int(l[0][1])-1]
        if (l[1] == c0 or l[1] == c1) and c0 != c1:
            passed += 1
    return passed

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
            grid = [[l[0].split('-'), l[1][0], l[2]] for l in lines]
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

