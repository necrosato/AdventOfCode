import time
import sys

cmap = {'=': -2, '-': -1, '0':0, '1':1, '2':2}
nmap = {-2: '=', -1: '-', 0:'0', 1:'1', 2:'2'}
numbers = [-2, -1, 0, 1, 2]

def addDigits(lines):
    digits = []
    for line in lines:
        for i in range(len(line)):
            if i == len(digits):
                digits.append(0)
            digits[i] += cmap[line[-(i+1)]]
    return (digits, sum([ digits[i]*5**i for i in range(len(digits)) ]))

def part1( lines ):
    digits, dsum = addDigits(lines)
    i = 0
    while True:
        rollover = int(float(digits[i] + (2 if digits[i] >= 0 else -2)) / 5)
        remainder = numbers[(digits[i] + 2) % 5]
        print(digits)
        print('digit index {} value {} rollover {} remainder {}\n'.format(i, digits[i], rollover, remainder))
        digits[i] = remainder
        if i == len(digits)-1:
            if rollover == 0:
                assert dsum == sum([ digits[i]*5**i for i in range(len(digits)) ])
                return ''.join(reversed([nmap[d] for d in digits]))
            else:
                digits.append(0)
        digits[i+1] += rollover
        i+=1

def part2( lines ):
    pass
    
for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        p1 = time.time()
        sol1 = part1(lines)
        p2 = time.time()
        sol2 = part2(lines)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
