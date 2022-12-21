import time
import sys

def mix( reference, numbers ):
    for i in range(len(reference)):
        source = numbers.index(reference[i])
        n = numbers.pop(source)
        target = (source+n[1]) % len(numbers)
        numbers.insert(target, n)
    return [n[1] for n in numbers]
 
def part1( reference ):
    reference = [(i, reference[i]) for i in range(len(reference))]
    mixed = mix(reference, [n for n in reference])
    return sum([mixed[(mixed.index(0) + i)%len(mixed)] for i in [1000, 2000, 3000]])

def part2( reference ):
    reference = [(i, reference[i]*811589153) for i in range(len(reference))]
    numbers = [n for n in reference]
    for k in range(10):
        mixed = mix(reference, numbers)
    return sum([mixed[(mixed.index(0) + i)%len(mixed)] for i in [1000, 2000, 3000]])

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
