elves = {1: 0}
i = 1
with open('input2.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if line != '':
            elves[i] += int(line)
        else:
            i+=1
            elves[i] = 0
print('part 1: ' + str(list(reversed(sorted(elves.items(), key=lambda item: item[1])))[0]))
print('part 2: ' + str(sum([e[1] for e in list(reversed(sorted(elves.items(), key=lambda item: item[1])))[0:3]])))
