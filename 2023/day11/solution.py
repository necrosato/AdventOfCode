import argparse
import time
import sys

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

def get_galaxies(grid):
    galaxies = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '#':
                galaxies.append((r, c))
    return galaxies
    
@timer_func
def part( galaxies, expand_rows, expand_cols, expand_len ):
    total = 0
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            for r in range(galaxies[i][0], galaxies[j][0], 1 if galaxies[i][0] < galaxies[j][0] else -1):
                total += expand_len if r in expand_rows else 1
            for c in range(galaxies[i][1], galaxies[j][1], 1 if galaxies[i][1] < galaxies[j][1] else -1):
                total += expand_len if c in expand_cols else 1
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            galaxies = get_galaxies(lines)
            expand_rows = set()
            for r in range(len(lines)):
                if set(lines[r]) == {'.'}:
                    expand_rows.add(r)
            expand_cols = set()
            for c in range(len(lines[0])):
                if { lines[r][c] for r in range(len(lines)) } == {'.'}:
                    expand_cols.add(c)
            sol1 = part(galaxies, expand_rows, expand_cols, 2)
            sol2 = part(galaxies, expand_rows, expand_cols, 1000000)
        
if __name__=='__main__':
    main()

