import time 
start = time.time()
elves = {1: 0}
i = 1
with open('input2.txt', 'r') as f:
    for line in [l.strip() for l in f.readlines()]:
        if line != '':
            elves[i] += int(line)
        else:
            i+=1
            elves[i] = 0
by_cals = list(reversed(sorted(elves.items(), key=lambda item: item[1])))
print('part 1: ' + str(by_cals[0]))
print('part 2: ' + str(sum([e[1] for e in by_cals[0:3]])))
end = time.time()
print('Took {} seconds'.format(end-start))
