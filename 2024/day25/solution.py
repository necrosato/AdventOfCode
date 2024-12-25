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

def overlap(lock,key):
    s = tuple(x + y for x, y in zip(lock, key))
    for i in s:
        if i > 5:
            return True
    return False

def heights(schematic, lock=True):
    h = [0]*len(schematic[0])
    s = schematic
    if not lock:
        s = reversed(schematic)
    for i, r in enumerate(s, start=0):
        for j, c in enumerate(r):
            if c == '#':
                h[j] = i
    return h

@timer_func
def part1( schematics ):
    lock_heights = []
    key_heights = []
    for s in schematics:
        if not '.' in s[-1] and not '#' in s[0]:
            key_heights.append(heights(s, lock=False))
        if not '#' in s[-1] and not '.' in s[0]:
            lock_heights.append(heights(s, lock=True))
    total = 0
    for lock in lock_heights:
        for key in key_heights:
            total += not overlap(lock, key)
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            schematics = [s.split('\n') for s in f.read().strip().split('\n\n')]
            sol1 = part1(schematics)
         
if __name__=='__main__':
    main()

