import argparse
import time
from collections import deque
import heapq
from itertools import combinations

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

@timer_func
def part1( wires, gates ):
    ops = {
            'AND': lambda x,y: x&y,
            'OR': lambda x,y: x|y,
            'XOR': lambda x,y: x^y
            }
    all_wires = set()
    for i1,op,i2,ar,dest in gates:
        all_wires |= set((i1,i2,dest))
    while not all_wires.issubset(set(wires.keys())):
        for i1,op,i2,ar,dest in gates:
            if i1 in wires and i2 in wires:
                wires[dest] = ops[op](wires[i1],wires[i2])
    res = ''
    for wire in reversed(sorted(wires)):
        if wire[0] == 'z':
            res += str(wires[wire])
    return int(res,2)

# Function to find the corresponding register for an expression
def find_expression(op1, op, op2, registers):
    for key, val in registers.items():
        if val == f'{op1} {op} {op2}' or val == f'{op2} {op} {op1}':
            return key
    return None

@timer_func
def part2( registers ):
    swaps = []
    index = 0
    carry_reg = ''
    while f'x{index:02d}' in registers and len(swaps) < 8:
        x_reg = f'x{index:02d}'
        y_reg = f'y{index:02d}'
        z_reg = f'z{index:02d}'

        if index == 0:
            carry_reg = find_expression(x_reg, 'AND', y_reg, registers)
        else:
            xor_reg = find_expression(x_reg, 'XOR', y_reg, registers)
            and_reg = find_expression(x_reg, 'AND', y_reg, registers)
            carry_in_reg = find_expression(xor_reg, 'XOR', carry_reg, registers)

            if carry_in_reg is None:
                swaps.extend([xor_reg, and_reg])
                registers[xor_reg], registers[and_reg] = registers[and_reg], registers[xor_reg]
                index = 0
                continue

            if carry_in_reg != z_reg:
                swaps.extend([carry_in_reg, z_reg])
                registers[carry_in_reg], registers[z_reg] = registers[z_reg], registers[carry_in_reg]
                index = 0
                continue

            carry_in_reg = find_expression(xor_reg, 'AND', carry_reg, registers)
            carry_reg = find_expression(and_reg, 'OR', carry_in_reg, registers)
        index += 1
    return ','.join(sorted(swaps))

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            p1,p2 = f.read().split('\n\n')
            wires = [l.split(': ') for l in p1.strip().split('\n')]
            wires = {k:int(v) for k,v in wires}
            gates = [l.split() for l in p2.strip().split('\n')]
            registers = {}
            for line in p1.splitlines():
                name, value = line.split(': ')
                registers[name] = value
            for line in p2.splitlines():
                value, name = line.split(' -> ')
                registers[name] = value
            sol1 = part1(wires, gates)
            sol2 = part2(registers)
         
if __name__=='__main__':
    main()

