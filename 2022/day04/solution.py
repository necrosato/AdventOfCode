import time

def splitup(line, delims):
    if len(delims) == 0:
        return line
    return [splitup(l, delims[1:]) for l in line.split(delims[0])]

def count(line):
    parts = splitup(line, [',', '-'])
    s11 = int(parts[0][0])
    s12 = int(parts[0][1])
    s21 = int(parts[1][0])
    s22 = int(parts[1][1])
    if ( s22 >= s12 and s21 <= s11 ):
        return 1
    if ( s22 <= s12 and s21 >= s11 ):
        return 1
    return 0

def count2(line): 
    s1, s2 = line.split(',')
    s11 = int(s1.split('-')[0])
    s12 = int(s1.split('-')[1])
    s21 = int(s2.split('-')[0])
    s22 = int(s2.split('-')[1])
    if ( s12 >= s21 and s11 <= s22 ):
        return 1
    if ( s12 <= s21 and s11 >= s22 ):
        return 1
    return 0

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        start = time.time()
        for line in [l.strip() for l in f.readlines()]:
            solution += count(line)
            solution2 += count2(line)
        end = time.time()
    print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
