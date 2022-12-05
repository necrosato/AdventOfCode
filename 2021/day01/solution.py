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
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        start = time.time()
        lines = [l.strip() for l in f.readlines()]
        last = 1000000000 
        for i in range(len(lines)-1):
            solution += count([lines[i], lines[i+1]])
        for i in range(len(lines)-2):
            this = count2([lines[i], lines[i+1], lines[i+2]])
            if this > last:
                solution2+=1
            last = this

        end = time.time()
    print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
