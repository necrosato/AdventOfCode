import time

def find_common(line):
    h1 = set()
    h2 = set()
    for i in range(len(line)):
       char = line[i]
       if i >= len(line)//2:
           h1.add(char)
       else:
           h2.add(char)
    char = next(iter(h1.intersection(h2)))
    offset = 64-26 if char.upper() == char  else 96
    print(char)
    return ord(char) - offset

with open('input2.txt', 'r') as f:
    start = time.time()
    part1 = 0
    part2 = 0
    for line in [l.strip() for l in f.readlines()]:
        part1 += find_common(line)
        print(part1)
    end = time.time()

print('part 1: {} part 2: {} took {} seconds'.format(part1, part2, end-start))
