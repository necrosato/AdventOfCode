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

def vector_add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                return (i, j, val)

def grid_find_all(grid, val):
    vals = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                vals.append((i, j, val))
    return vals
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()


def shift(grid, at, move):
    nl = []
    lv = None
    while lv != '.': 
        if lv is None:
            lv = '.'
        tmp = grid[at[0]][at[1]]
        grid[at[0]][at[1]] = lv
        lv = tmp
        at = vector_add(at, move)

def next_list(grid, at, move):
    nl = []
    while grid[at[0]][at[1]] not in ['#', '.']:
        at = vector_add(at, move)
        nl.append(grid[at[0]][at[1]])
    return nl

dirs = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
@timer_func
def part1( grid, moves ):
    at = grid_find(grid, '@')
    for move in ''.join(moves):
        if next_list(grid, at, dirs[move])[-1] == '.':
            shift(grid, at, dirs[move])
            at = vector_add(at, dirs[move])
    total = 0
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 'O':
                total += (100*i)+j
    return total

def has_free(grid, at, move, mem):
    if at in mem:
        return mem[at]
    np = vector_add(at, move)
    c = grid[np[0]][np[1]]
    nps = []
    if c == ']':
        nps.append(vector_add(np, (0, -1)))
    elif c == '[':
        nps.append(vector_add(np, (0, 1)))
    elif c == '#':
        mem[at] = False
        return False
    elif c == '.':
        mem[at] = True
        return True
    nps.append(np)
    frees = [has_free(grid, np, move, mem) for np in nps]
    mem[at] = False not in frees
    return mem[at]
    

tf = {'#':'##', 'O':'[]', '.':'..', '@':'@.'}
@timer_func
def part2( grid, moves ):
    ng = []
    for line in grid:
        nl = []
        for c in line:
            nl += list(tf[c])
        ng.append(nl)
    grid = ng
    at = grid_find(grid, '@')[:-1]
    for move in ''.join(moves):
        if move in ['^','v']:
            mem = {}
            if has_free(grid, at, dirs[move], mem):
                cols = {}
                for i, j in mem.keys():
                    if j not in cols:
                        cols[j] = set()
                    cols[j].add(i)
                for j in cols:
                    for i in cols[j]:
                        if i-dirs[move][0] not in cols[j]:
                            shift(grid, (i, j), dirs[move])
                at = vector_add(at, dirs[move])
        else:
            if next_list(grid, at, dirs[move])[-1] == '.':
                shift(grid, at, dirs[move])
                at = vector_add(at, dirs[move])
    total = 0
    for box in grid_find_all(grid, '['):
        total += 100*box[0]+box[1]
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            g, moves = f.read().split('\n\n')
            grid = list(map(list,g.split('\n')))
            grid2 = list(map(list,g.split('\n')))
            moves = moves.split('\n')
            sol1 = part1(grid, moves)
            sol2 = part2(grid2, moves)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

