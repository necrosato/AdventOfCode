import time
import sys

def yell( monkey, monkeys, memo ):
    if len(monkeys[monkey]) == 1:
        v = monkeys[monkey][0]
    else:
        l = yell(monkeys[monkey][0], monkeys, memo)
        r = yell(monkeys[monkey][2], monkeys, memo)
        op = monkeys[monkey][1]
        if op == '+':
            v = l + r
        if op == '-':
            v = l - r
        if op == '*':
            v = l * r
        if op == '/':
            v = l // r
    memo[monkey] = v
    return memo[monkey]

def contains(monkey, check, monkeys):
    if monkey == check:
        return True
    if len(monkeys[monkey]) > 1:
        return contains(monkeys[monkey][0], check, monkeys) or contains(monkeys[monkey][2], check, monkeys)
    return False

def part2( monkeys ):
    check = monkeys['root'][0]
    target = yell(monkeys['root'][2], monkeys, {})
    if contains(monkeys['root'][2], 'humn', monkeys):
        check = monkeys['root'][2]
        target = yell(monkeys['root'][0], monkeys, {})
    factor = 10000000000
    val = target+1
    while factor > 0:
        while val > target:
            monkeys['humn'][0] += factor
            val = yell(check, monkeys, {})
            print('humn {} val {} target {} diff {} factor {}'.format( monkeys['humn'][0], val, target, target-val, factor))
        monkeys['humn'][0] -= factor
        factor //= 10
        val = yell(check, monkeys, {})
    return monkeys['humn'][0] + 1

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        monkeys = {}
        for line in lines:
            name, instructions = line.split(': ')
            instructions = instructions.split()
            if len(instructions) == 1:
                instructions = [int(instructions[0])]
            monkeys[name] = instructions
        p1 = time.time()
        sol1 = yell('root', monkeys, {})
        p2 = time.time()
        sol2 = part2(monkeys)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
