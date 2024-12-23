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
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

ops = {'>': lambda x,y: x>y,
       '<': lambda x,y: x<y}
memo = {}
def check(xmas, workflow, workflows):
    if (xmas, workflow) in memo:
        return memo[(xmas, workflow)]
    xmases = { x:v for x,v in xmas}
    if workflow in ['A','R']:
        return workflow
    for rule in workflows[workflow]:
        if len(rule) == 2:
            l = rule[0][0]
            c = rule[0][1]
            i = int(rule[0][2:])
            if ops[c](xmases[l],i):
                final_dest = check(xmas, rule[-1], workflows)
                break
        if len(rule) == 1:
            final_dest = check(xmas, rule[-1], workflows)
    memo[(xmas, workflow)] = final_dest
    return final_dest

def paths(workflows):
    paths = [[['in', set()]]]
    final_paths = []
    while paths:
        np = []
        for path in paths:
            if path[-1][0] == 'A':
                final_paths.append(path)
            elif path[-1][0] != 'R':
                falserules = set()
                for rule in workflows[path[-1][0]]:
                    rules = path[-1][-1] | falserules
                    rules.add('&'+rule[0])
                    np.append(path + [(rule[-1], rules)])
                    falserules.add('!'+rule[0])
        paths = np
    return final_paths

def get_intervals(path, workflows):
    intervals = {c: [1, 4000] for c in 'xmas'}
    for rule in path[-1][-1]:
        if '>' in rule or '<' in rule:
            do = rule[0] == '&'
            l = rule[1]
            c = rule[2]
            i = int(rule[3:])
            if c == '>' and do:
                intervals[l][0] = max(intervals[l][0], i+1)
            if c == '<' and not do:
                intervals[l][0] = max(intervals[l][0], i)
            if c == '<' and do:
                intervals[l][1] = min(intervals[l][1], i-1)
            if c == '>' and not do:
                intervals[l][1] = min(intervals[l][1], i)
    return intervals
        
@timer_func
def part1( workflows, xmases ):
    total = 0
    for xmas in xmases:
        c = check(xmas, 'in', workflows)
        if c == 'A':
            for k,v in xmas:
                total += v
    return total

@timer_func
def part2( workflows, xmases ):
    total = 0
    for path in paths(workflows):
        pcount = 1
        for minval,maxval in get_intervals(path, workflows).values():
            pcount *= maxval-minval+1
        total += pcount 
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            workflow_lines, vals = f.read().split('\n\n')
            workflows = {}
            for line in workflow_lines.split():
                name, rules = line.split('{') 
                rules = list(map(lambda x: tuple(x.split(':')), rules[:-1].split(',')))
                workflows[name] = rules
            xmases = []
            for line in vals.split():
                xmases.append(tuple((pair.split('=')[0], int(pair.split('=')[1])) for pair in line[1:-1].split(',')))
            sol1 = part1(workflows, xmases)
            sol2 = part2(workflows, xmases)
         
if __name__=='__main__':
    main()

