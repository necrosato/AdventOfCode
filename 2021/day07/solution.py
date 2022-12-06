import time

for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        start = time.time()
        crabs = [int(n) for n in f.readlines()[0].strip().split(',')]
        costs = {}
        costs2 = {}
        for h in range(min(crabs), max(crabs)):
            costs[h] = sum([abs(crab-h) for crab in crabs])
            costs2[h] = sum([sum(range(abs(crab-h)+1)) for crab in crabs])
        solution = list(sorted(costs.items(), key=lambda pair: pair[1]))[0][1]
        print(list(sorted(costs2.items(), key=lambda pair: pair[1]))[0][0])
        solution2 = list(sorted(costs2.items(), key=lambda pair: pair[1]))[0][1]

        end = time.time()
    print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
