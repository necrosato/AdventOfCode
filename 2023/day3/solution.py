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

def border(grid, ii, jj):
    b = []
    for i in range(ii-1, ii+2):
        for j in range(jj-1, jj+2):
            if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[i]):
                b.append((i, j))
    return b
def part_number(grid, k, l):
    line = grid[k]
    start = l
    for i in range(l-1, -1, -1):
        if not line[i].isnumeric():
            break
        start = i
    end = l
    for i in range(l+1, len(line)+1):
        end = i
        if i == len(line) or not line[i].isnumeric():
            break
    return (k, start, end, int(line[start:end]))
@timer_func
def part1( grid ):
    pns = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] not in '1234567890.':
                b = border(grid, i, j)
                for k,l in b:
                    if grid[k][l].isnumeric():
                        pn = part_number(grid, k, l)
                        pns.add(pn)
    return sum([l[-1] for l in pns])

@timer_func
def part2( grid ):
    ratio_sum = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '*':
                pns = set()
                b = border(grid, i, j)
                ratio = 1
                count = 0
                for k,l in b:
                    if grid[k][l].isnumeric():
                        pn = part_number(grid, k, l)
                        pns.add(pn)
                for pn in pns:
                    ratio *= pn[-1]
                    count += 1
                if count == 2:
                    ratio_sum += ratio
    return ratio_sum


def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = lines
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

