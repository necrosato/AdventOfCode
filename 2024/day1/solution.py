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
    l1 = sorted([int(grid[i][0]) for i in range(len(grid))])
    l2 = sorted([int(grid[i][1]) for i in range(len(grid))])
    dists = [abs(l1[i] - l2[i]) for i in range(len(grid))]
    return sum(dists)

def make_occurrences(l):
    occurrences = {}
    for i in l:
        if i not in occurrences:
            occurrences[i] = 1
        else:
            occurrences[i] += 1
    return occurrences

def similarity(i, occ):
    return i*(0 if i not in occ else occ[i])

@timer_func
def part2( grid ):
    l1 = [int(grid[i][0]) for i in range(len(grid))]
    l2 = [int(grid[i][1]) for i in range(len(grid))]
    l2o = make_occurrences(l2)
    similarities = [similarity(i, l2o) for i in l1]
    return sum(similarities)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = [l.split() for l in lines]
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

