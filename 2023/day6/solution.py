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
def part1( times,dists ):
    total = 1
    for i in range(len(times)):
        race = 0
        for seconds in range(times[i]+1):
            speed = seconds
            dist = speed * (times[i] - seconds)
            if dist > dists[i]:
                race += 1
        total *= race
    return total

@timer_func
def part2( times,dists ):
    pass

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            times = [ int(n) for n in lines[0].strip().split()[1:] ]
            dists = [ int(n) for n in lines[1].strip().split()[1:] ]
            sol1 = part1(times,dists)
            times = [ int( ''.join(lines[0].strip().split()[1:]) ) ]
            dists = [ int( ''.join(lines[1].strip().split()[1:]) ) ]
            sol2 = part1(times,dists)
        
if __name__=='__main__':
    main()

