import argparse
import time
from collections import deque
import heapq
import copy

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
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def in_range(grid, coords):
    return coords[0] in range(len(grid)) and coords[1] in range(len(grid[0]))

def next_pos(beam):
    return vector_add(beam[0], beam[1])
dirs =[(-1, 0),(0, 1),(1, 0),(0, -1)]
def splitv(beam, op):
    if beam[1][0] == 0: 
        return [move((beam[0], (-1, 0))), move((beam[0], (1, 0)))]
    return [move(beam)]
def splith(beam, op):
    if beam[1][1] == 0: 
        return [move((beam[0], (0, -1))), move((beam[0], (0, 1)))]
    return [move(beam)]
def rotate(beam, op):
    for i, d in enumerate(dirs):
        if beam[1] == d:
            if op == '/':
                if beam[1][1] == 0:
                    return [move((beam[0], dirs[(i+1)%len(dirs)]))]
                return [move((beam[0], dirs[(i-1)%len(dirs)]))]
            elif op == '\\':
                if beam[1][0] == 0:
                    return [move((beam[0], dirs[(i+1)%len(dirs)]))]
                return [move((beam[0], dirs[(i-1)%len(dirs)]))]
def move(beam):
    return (next_pos(beam), beam[1])

actions = {
        '|':splitv,
        '-':splith,
        '\\':rotate,
        '/':rotate,
        '.':lambda x,y: [move(x)] 
        }
        
def energized(start_beam, grid):
    beams = [start_beam]
    seen = set()
    last = None
    energized = set()
    while beams:
        temp = []
        for i, beam in enumerate(beams):
            if in_range(grid, beam[0]) and beam not in seen:
                seen.add(beam)
                energized.add(beam[0])
                c = grid[beam[0][0]][beam[0][1]]
                temp += actions[c](beam, c)
        beams = temp
    return len(energized)

@timer_func
def part1( grid ):
    beam = ((0, 0), (0, 1))
    return energized(beam, grid)
@timer_func
def part2( grid ):
    energized_map = {}
    start_beams = []
    for i in range(len(grid)):
        for j in [0, len(grid[0])]:
            if j == 0: 
                start_beams.append(((i, j), (0, 1)))
            else:
                start_beams.append(((i, j), (0, -1)))
    for i in [0, len(grid)]:
        for j in range(len(grid[0])):
            if i == 0: 
                start_beams.append(((i, j), (1, 0)))
            else:
                start_beams.append(((i, j), (-1, 0)))
    for b, start_beam in enumerate(start_beams):
        energized_map[start_beam] = energized(start_beam, grid) 
    return max(energized_map.values())

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [list(l.strip()) for l in f.readlines()]
            sol1 = part1(grid)
            sol2 = part2(grid)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

