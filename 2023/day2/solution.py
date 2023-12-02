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
def part1( lines ):
    bag = { 'red': 12, 'green': 13, 'blue': 14}
    validSum = 0
    for line in lines:
        valid = True
        print(line)
        gn, g = line.split(': ')
        gn = int(gn.split()[1])
        rounds = g.split('; ')
        for r in rounds:
            r = r.split(', ')
            for p in r:
                cn, c = p.split()
                cn = int(cn)
                if bag[c] < cn:
                    valid = False
                    break

        if valid:
            validSum += gn
    return validSum 

@timer_func
def part2( lines ):
    bag = { 'red': 12, 'green': 13, 'blue': 14}
    powerSum = 0
    for line in lines:
        maxes = { 'red': 0, 'green': 0, 'blue': 0}
        gn, g = line.split(': ')
        gn = int(gn.split()[1])
        rounds = g.split('; ')
        for r in rounds:
            r = r.split(', ')
            for p in r:
                cn, c = p.split()
                cn = int(cn)
                maxes[c] = max(maxes[c], cn)
            power = maxes['red'] * maxes['green'] * maxes['blue']
        powerSum += power
    return powerSum 

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            sol1 = part1(lines)
            sol2 = part2(lines)
        
if __name__=='__main__':
    main()
