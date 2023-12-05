import argparse
import time
import re

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
def split_on_empty_lines(s):
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())

def range_intersect(x, y):
    if x[-1] < y[0] or y[-1] < x[0]:
        return None
    return range(max(x[0], y[0]), min(x[-1], y[-1])+1)

# returns [] if x contains y entirely, 1 range if x contains y partially, 2 ranges if y contains x entirely
def range_overlaps(x, y):
    overlaps = []
    if x[0] > y[0]:
        overlaps.append(range(y[0], x[0]+1))
    if y[-1] > x[-1]:
        overlaps.append(range(x[-1]+1, y[-1]+1))
    return overlaps

@timer_func
def part1( seeds, maps ):
    lowloc = None
    for seed in seeds:
        index = seed
        for m in maps:
            index_old = index
            for r in m[-1]:
                if index in r:
                    index = m[-1][r][r.index(index)]
                    break
            print('seed {} {} to {}: {} {}'.format(seed, m[0], m[1], index_old, index))
        if lowloc == None or lowloc > index:
            lowloc = index
    return lowloc

@timer_func
def part2( seedranges, maps ):
    ranges_input = seedranges
    for m in maps:
        ranges_mapped = []
        for sr in m[-1]:
            dr = m[-1][sr]
            ranges_output = []
            for ir in ranges_input:
                intersect = range_intersect(sr, ir)
                if intersect is not None:
                    drm = dr[sr.index(intersect[0]):sr.index(intersect[-1])+1]
                    ranges_mapped.append(drm)
                    ranges_output = ranges_output + range_overlaps(sr, ir)
                else:
                    ranges_output.append(ir)
            ranges_input = ranges_output
        ranges_input = ranges_mapped + ranges_input
        print('{} to {}: {}'.format(m[0], m[1], ranges_input))
    return min([r[0] for r in ranges_input])

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = split_on_empty_lines(f.read())
            seeds = list(map(lambda x: int(x), lines[0].strip().split()[1:]))
            maps = []
            for block in [ l.split('\n') for l in lines[1:] ]:
                source, dest = block[0].split(' map')[0].split('-to-')
                sdm = {}
                for line in block[1:]:
                    drs, srs, rl = list(map(lambda x: int(x), line.strip().split()))
                    sr = range(srs, srs+rl)
                    dr = range(drs, drs+rl)
                    sdm[sr] = dr
                maps.append([source, dest, sdm])
            sol1 = part1(seeds,maps)
            seedranges = [range(seeds[i], seeds[i] + seeds[i+1]) for i in range(0, len(seeds), 2)]
            sol2 = part2(seedranges,maps)
        
if __name__=='__main__':
    main()
