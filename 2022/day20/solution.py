import math
import time
import sys

def part1( reference ):
    reference = [(i, reference[i]) for i in range(len(reference))]
    numbers = [n for n in reference]
    for i in range(len(reference)):
        source = numbers.index(reference[i])
        n = numbers.pop(source)
        target = (source+n[1]) % len(numbers)
        numbers.insert(target, n)
    numbers = [n[1] for n in numbers]
    return sum([numbers[(numbers.index(0) + i)%len(numbers)] for i in [1000, 2000, 3000]])

def part2( reference ):
    key = 811589153
    reference = [(i, reference[i]*key) for i in range(len(reference))]
    numbers = [n for n in reference]
    for k in range(10):
        for i in range(len(reference)):
            source = numbers.index(reference[i])
            n = numbers.pop(source)
            target = (source+n[1]) % len(numbers)
            numbers.insert(target, n)
    numbers = [n[1] for n in numbers]
    return sum([numbers[(numbers.index(0) + i)%len(numbers)] for i in [1000, 2000, 3000]])


for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        original = [int(line) for line in lines]
        p1 = time.time()
        sol1 = part1(original)
        p2 = time.time()
        sol2 = part2(original)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
