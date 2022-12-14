import time
import sys

def part1( grid ):
    pass
def part2( grid ):
    pass

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        grid = [[(charHeight(c),c) for c in line] for line in lines]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == (1,'S'):
                    src = (i, j)
                if grid[i][j] == (26,'E'):
                    dst = (i, j)
        p1 = time.time()
        sol1 = part1(grid)
        p2 = time.time()
        sol2 = part2(grid)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
