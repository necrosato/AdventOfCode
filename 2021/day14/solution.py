import time
import copy

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        sequence = lines[0]
        instructions = {}
        for line in lines[2:]:
            t,f = line.split(' -> ')
            instructions[t] = f
        steps = 40
        memo = {}
        memochars = {}
        for char in sequence:
            if char not in memochars:
                memochars[char] = 0
            memochars[char] += 1
        for i in range(len(sequence)-1):
            memo[sequence[i:i+2]] = 1
        for i in range(steps):
            tmp = copy.deepcopy(memo)
            for pair in memo:
                if tmp[pair] > 0:
                    tmp[pair] -= memo[pair]
                    if tmp[pair] == 0:
                        tmp.pop(pair)
                    subs = [pair[0] + instructions[pair], instructions[pair] + pair[1]]
                    if instructions[pair] not in memochars:
                        memochars[instructions[pair]] = 0
                    memochars[instructions[pair]] += memo[pair]
                    for p in subs:
                        if p not in tmp:
                            tmp[p] = 0
                        tmp[p] += memo[pair]
            memo = tmp

        charCounts = list(sorted(memochars.items(), key=lambda x: x[1]))
        print(charCounts)
        solution = charCounts[-1][1] - charCounts[0][1]
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
