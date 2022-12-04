import time

def splitup(line, delims):
    if len(delims) == 0:
        return line
    return [splitup(l, delims[1:]) for l in line.split(delims[0])]

def count(line):
    return 0

def count2(line):
    return 0

for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        solution = 0
        solution2 = 0
        start = time.time()
        for line in [l.strip() for l in f.readlines()]:
            solution += count(line)
            solution2 += count2(line)
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
