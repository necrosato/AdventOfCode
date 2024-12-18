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

def run_program(a, b, c, program):
    ip = 0
    max_ip = len(program)-2
    output=[]
    while ip <= max_ip:
        opcode = program[ip]
        operand = program[ip+1]
        combo = None
        if operand in [0, 1, 2, 3]:
            combo = operand
        elif operand == 4:
            combo = a
        elif operand == 5:
            combo = b
        elif operand == 6:
            combo = c

        if opcode == 0:
            a = a//(2**combo)
        if opcode == 1:
            b = b^operand
        if opcode == 2:
            b = combo%8 
        if opcode == 3:
            if a != 0:
                ip = combo-2
        if opcode == 4:
            b=b^c
        if opcode == 5:
            output.append(combo%8)
        if opcode == 6:
            b = a//(2**combo)
        if opcode == 7:
            c = a//(2**combo)
        ip+=2
    return output

@timer_func
def part1(a, b, c, program):
    output = run_program(a, b, c, program)
    return ','.join(list(map(str,output)))

def output(n):
    partial = (n%8)^2
    return ((partial ^ (n >> partial)) ^ 7) % 8

def solve(a, program):
    meta_inputs = { 0 }
    for num in reversed(program):
        new_meta_inputs = set()
        for curr_num in meta_inputs:
            for new_segment in range(8):
                new_num = (curr_num << 3) + new_segment
                if output(new_num) == num:
                    new_meta_inputs.add(new_num)
        meta_inputs = new_meta_inputs
    return min(meta_inputs)

@timer_func
def part2(a, b, c, program):
    return solve(a, program)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [l.strip() for l in f.readlines()]
            a = int(grid[0].split()[-1])
            b = int(grid[1].split()[-1])
            c = int(grid[2].split()[-1])
            program = list(map(int, grid[4].split()[-1].split(',')))
            sol1 = part1(a, b, c, program)
            sol2 = part2(a, b, c, program)
         
if __name__=='__main__':
    main()

