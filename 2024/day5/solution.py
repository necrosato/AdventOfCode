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


def is_broken(rules, update):
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) >= update.index(rule[1]):
                return True
    return False
 
@timer_func
def part1( grid ):
    rules = []
    updates = []
    for line in grid:
        if '|' in line:
            rules.append(list(map(int,line.split('|'))))
        elif line != '':
            updates.append(list(map(int,line.split(','))))
    valid = 0
    for update in updates:
        if not is_broken(rules, update):
            valid += update[len(update)//2]
    return valid

@timer_func
def part2( grid ):
    rules = []
    updates = []
    for line in grid:
        if '|' in line:
            rules.append(list(map(int,line.split('|'))))
        elif line != '':
            updates.append(list(map(int,line.split(','))))
    valid = 0
    rmap = {}
    for rule in rules:
        a,b = rule
        if a not in rmap:
            rmap[a] = [set(), set()]
        if b not in rmap:
            rmap[b] = [set(), set()]
        rmap[a][1].add(b) 
        rmap[b][0].add(a) 
    for update in updates:
        if is_broken(rules,update):
            temp = list(update)
            while is_broken(rules, temp):
                for c in temp:
                    if c in rmap:
                        i = temp.index(c)
                        breaking = (rmap[c][0] & set(temp[i+1:])) | (rmap[c][1] & set(temp[:i]))
                        if breaking:
                            wi = temp.index(min(breaking))
                            temp[i], temp[wi] = temp[wi], temp[i]
            valid += temp[len(temp)//2]
    return valid

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

