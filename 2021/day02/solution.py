import time

def splitup(line, delims):
    if len(delims) == 0:
        return line
    return [splitup(l, delims[1:]) for l in line.split(delims[0])]

def count(pair):
    if int(pair[1]) > int(pair[0]):
        return 1
    return 0

def count2(lines): 
    return sum([int(l.split()[0]) for l in lines])

for fname in ['input.txt', 'input2.txt']:
    solution = [0, 0]
    solution2 = [0, 0, 0]
    with open(fname, 'r') as f:
        start = time.time()
        for line in [l.strip().split() for l in f.readlines()]:
            if line[0] == 'forward':
                solution[0] += int(line[1])
                solution2[0] += int(line[1])
                solution2[1] += int(line[1]) * solution2[2]
            if line[0] == 'up':
                solution[1] -= int(line[1])
                solution2[2] -= int(line[1])
            if line[0] == 'down':
                solution[1] += int(line[1])
                solution2[2] += int(line[1])
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution[0]*solution[1], solution2[0]*solution2[1], end-start))
