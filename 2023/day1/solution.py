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
    digits = []
    for l in grid:
        nl = ''
        for c in l:
            if ord(c) >= 48 and ord(c) <= 57:
                nl+=c
        digits.append(nl)
    s = 0
    for l in digits:
        s += int(l[0] + l[-1])
    return s

dwords = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
@timer_func
def part2( grid ):
    digits = []
    for l in grid:
        nl = ''
        for i in range(len(l)):
            c = l[i]
            if ord(c) >= 48 and ord(c) <= 57:
                nl+=c
            for j in range(len(dwords)):
                dw = dwords[j]
                ei = i+len(dw)
                if ei <= len(l):
                    if l[i:ei] == dw:
                        nl+= str(j+1)
        digits.append(nl)
    s = 0
    for l in digits:
        s += int(l[0] + l[-1])
        print(int(l[0] + l[-1]))
    return s

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = lines
            #sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

