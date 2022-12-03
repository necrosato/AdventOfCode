import time

def find_common(line1, line2, line3):
    sets = [set(), set(), set()]
    for j in range(3):
        line = [line1, line2, line3][j]
        for i in range(len(line)):
           char = line[i]
           if i >= len(line)//2:
               sets[j].add(char)
           else:
               sets[j].add(char)
    char = next(iter(sets[0].intersection(sets[1].intersection(sets[2]))))
    offset = 64-26 if char.upper() == char  else 96
    print(char)
    return ord(char) - offset

with open('input.txt', 'r') as f:
    start = time.time()
    part1 = 0
    part2 = 0
    lines = [l.strip() for l in f.readlines()]
    for i in range(0, len(lines), 3):
        line1, line2, line3 = lines[i:i+3]
        part1 += find_common(line1, line2, line3)
        print(part1)
    end = time.time()

print('part 1: {} part 2: {} took {} seconds'.format(part1, part2, end-start))
