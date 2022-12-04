import time

def count(line): 
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
    with open(fname, 'r') as f:
        start = time.time()
        for line in [l.strip() for l in f.readlines()]:
            solution += count(line)
        end = time.time()
    print('{} solution: {} took {} seconds'.format(fname, solution, end-start))
