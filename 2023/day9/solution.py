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

def line_diffs(line):
    return [ line[i+1] - line[i] for i in range(len(line)-1) ]

def new_diffs(diffs_grid):
    diffs = [0]
    for i in range(len(diffs_grid)-2, -1, -1):
        diffs.append(diffs_grid[i][-1] + diffs[-1]) 
    return list(reversed(diffs))

def new_diffs2(diffs_grid):
    diffs = [0]
    for i in range(len(diffs_grid)-2, -1, -1):
        diffs.append(diffs_grid[i][0] - diffs[-1]) 
    return list(reversed(diffs))

@timer_func
def sum_diffs(grid, ndf):
    line_new_diffs = []
    for line in grid:
        diffs = line
        dgrid = [diffs]
        while set(diffs) != {0}:
            diffs = [ diffs[i+1] - diffs[i] for i in range(len(diffs)-1) ]
            dgrid.append(diffs)
        line_new_diffs.append(ndf(dgrid)[0])
    return sum(line_new_diffs)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [ [ int(n) for n in l.strip().split() ] for l in f.readlines()]
            sol1 = sum_diffs(grid, new_diffs)
            sol2 = sum_diffs(grid, new_diffs2)
        
if __name__=='__main__':
    main()
