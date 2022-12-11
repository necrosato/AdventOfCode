import time

for fname in ['input.txt', 'input2.txt']:
    regx = 1
    solution = 0
    solution2 = []
    for i in range(6):
        solution2.append(['.' for j in range(40)])
    i = 0
    cycles = 240
    toadd = 0
    checkCycles = set([20, 60, 100, 140, 180, 220])
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for cycle in range(1, cycles+1):
            if cycle in checkCycles:
                solution+=regx*cycle
            for s in range(regx-1, regx+2):
                if (cycle-1)%40 == s:
                    solution2[(cycle-1)//40][(cycle-1)%40] = '#'
            if toadd != 0:
                regx += toadd
                toadd = 0
            else:
                line = lines[i].split()
                if line[0] == 'addx':
                    toadd = int(line[1])
                i+=1
        end = time.time()
        solution2 = '\n'.join([''.join(row) for row in solution2])
        print('{} solution: {} solution2: \n{} took {} seconds'.format(fname, solution, solution2, end-start))
