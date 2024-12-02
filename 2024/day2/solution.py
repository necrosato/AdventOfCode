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

def is_increasing_or_decreasing(line):
    sl = sorted(line)
    return sl == line or sl == list(reversed(line))

def is_adjacent(line):
    for i in range(len(line)-1):
        if abs(line[i+1]-line[i]) not in range(1,4):
            return False
    return True

@timer_func
def part1( grid ):
    return sum([is_increasing_or_decreasing(line) and is_adjacent(line) for line in grid])

@timer_func
def part2( grid ):
    safe = 0
    for line in grid:
        if is_increasing_or_decreasing(line) and is_adjacent(line):
            safe += 1
        else:
            for i in range(len(line)):
                new_line = line[0:i] + line[i+1:]
                if is_increasing_or_decreasing(new_line) and is_adjacent(new_line):
                    safe += 1
                    break
    return safe

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = [[int(i) for i in line.strip().split()] for line in lines]
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

