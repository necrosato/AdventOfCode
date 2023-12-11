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

cmap = {
    '.': ((0, 0), (0, 0)),
    '|': ((-1, 0), (1, 0)),
    '-': ((0, -1), (0, 1)),
    'L': ((-1, 0), (0, 1)),
    'J': ((-1, 0), (0, -1)),
    '7': ((1, 0), (0, -1)),
    'F': ((1, 0), (0, 1)),
}
def connections(grid, row, col):
    return [(row+r, col+c) for r,c in cmap[grid[row][col]]]

def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                return (r, c)

def neighbors(grid, row, col):
    inside = []
    for r,c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if r < len(grid) and c < len(grid[r]):
            inside.append((r, c))
    return inside

def follow(grid, row, col, visited):
    current = (row, col)
    while current not in visited:
        visited.add(current)
        for c in connections(grid, *current):
            if c not in visited:
                current = c
    return visited

def get_path(grid):
    start = find_start(grid)
    visited = set()
    visited.add(start)
    for n in neighbors(grid, *start):
        for nc in connections(grid, *n):
            if nc == start:
                return follow(grid, *n, visited)


def gap_area(grid, path):
    area = 0
    for r in range(len(grid)):
        pruned = ''
        for c in range(len(grid[r])):
            pruned += grid[r][c] if (r,c) in path else '.'
        pruned = pruned.strip('.')
        pruned = pruned.replace('S', '7')
        pruned = pruned.replace('-', '')
        pruned = pruned.replace('F7', '')
        pruned = pruned.replace('LJ', '')
        pruned = pruned.replace('FJ', '|')
        pruned = pruned.replace('L7', '|')
        ps = pruned.split('|')
        for i in range(len(ps)):
            area += len(ps[i]) * (i%2)
    return area

@timer_func
def part1( grid ):
    return len(get_path(grid)) // 2

@timer_func
def part2( grid ):
    path = get_path(grid)
    return gap_area(grid, path)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [l.strip() for l in f.readlines()]
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()
