import argparse
import time
from collections import deque
import heapq
from math import gcd

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

class Module:
    def __repr__(self):
        return self.name
    def log(self):
        return '{} {} {} {}'.format(self.name, self.memory, self.inputs, self.outputs)
    def __init__(self, name, op):
        self.name = name
        self.op = op
        self.inputs = []
        self.outputs = []
        self.flipflop = False
        self.memory = {}
        self.low = 0
        self.high = 0
    def output(self, other):
        self.outputs.append(other)
        other.input(self)
    def input(self, other):
        self.inputs.append(other)
        self.memory[other.name] = False
    def pulse(self, from_module, high, queue):
        if high:
            self.high += 1
        else:
            self.low += 1
        self.memory[from_module] = high
        if self.op == '%' and not high:
            self.flipflop = not self.flipflop
            for module in self.outputs:
                queue.append([module, self.name, self.flipflop])
        elif self.op == '&':
            np = False if False not in self.memory.values() else True
            for module in self.outputs:
                queue.append([module, self.name, np])
        elif self.op == 'b':
            for module in self.outputs:
                queue.append([module, self.name, high])

@timer_func
def part1( modules ):
    for i in range(1000):
        queue = [[modules['broadcaster'], 'button', False]]
        while queue:
            queue[0][0].pulse(queue[0][1],queue[0][2], queue)
            queue.pop(0)
    return sum([modules[m].low for m in modules])*sum([modules[m].high for m in modules])

@timer_func
def part2( modules ):
    rx = False
    since_print = {m:0 for m in modules}
    loop = set()
    while not rx:
        for m in since_print:
            since_print[m] += 1
        queue = [[modules['broadcaster'], 'button', False]]
        while queue:
            if queue[0][0].name == 'gq' and queue[0][2]:
                if since_print[queue[0][1]] in loop:
                    rx = True
                else:
                    print(queue[0], queue[0][0].log(), since_print[queue[0][1]])
                    loop.add(since_print[queue[0][1]])
                    since_print[queue[0][1]] = 0
            queue[0][0].pulse(queue[0][1],queue[0][2], queue)
            queue.pop(0)
    lcm = 1
    for i in loop: 
        lcm = lcm*i//gcd(lcm,i)
    return lcm

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            modules = {}
            modules2 = {}
            for line in lines:
                name, out = line.split(' -> ')
                op = name[0]
                name = name[1:] if name[0] in ['%','&'] else name
                modules[name] = Module(name, op)
                modules2[name] = Module(name, op)
            for line in lines:
                name, out = line.split(' -> ')
                name = name[1:] if name[0] in ['%','&'] else name
                out = out.split(', ')
                for o in out:
                    if o not in modules:
                        modules[o] = Module(o, 'b')
                        modules2[o] = Module(o, 'b')
                    modules[name].output(modules[o])
                    modules2[name].output(modules2[o])
            sol1 = part1(modules)
            sol2 = part2(modules2)
         
if __name__=='__main__':
    main()

