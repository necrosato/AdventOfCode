import time

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for line in lines:
            pass
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
