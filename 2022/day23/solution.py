import time
import sys

directions = 'NSWE'
offsets = {'N': ([-1, 0, 1], [-1]), 'S': ([-1, 0, 1], [1]), 'W': ([-1], [-1, 0, 1]), 'E': ([1], [-1, 0, 1])}

def getFreeNeighbors(source, offset, elves):
    neighbors = [(source[0] + xo, source[1] + yo) for xo in offset[0] for yo in offset[1]]
    for neighbor in neighbors:
        if neighbor in elves:
            return []
    return neighbors

def shouldMove(x, y, elves):
    for nx in [x-1, x, x+1]:
        for ny in [y-1, y, y+1]:
            if nx != x or ny != y:
                if (nx, ny) in elves:
                    return True
    return False

def getDimensions(elves):
    return (1 + max([elf[0] for elf in elves]) - min([elf[0] for elf in elves]), 1 + max([elf[1] for elf in elves]) - min([elf[1] for elf in elves]))

def executeRound(elves, directions):
    propositions = {}
    movements = 0
    for elf in elves:
        if shouldMove(*elf, elves):
            for direction in directions:
                neighbors = getFreeNeighbors(elf, offsets[direction], elves)
                if len(neighbors) == 3:
                    if neighbors[1] not in propositions:
                        propositions[neighbors[1]] = []
                    propositions[neighbors[1]].append(elf)
                    break
    for spot in propositions:
        if len(propositions[spot]) == 1:
            elves.remove(propositions[spot][0])
            elves.add(spot)
            movements += 1
    return movements

def part1( elves ):
    i = 0
    while i < 10 and executeRound(elves, directions[i%4:4]+directions[0:i%4]) > 0:
        i+=1
    return getDimensions(elves)[0]*getDimensions(elves)[1] - len(elves)

def part2( elves ):
    i = 0
    while executeRound(elves, directions[i%4:4]+directions[0:i%4]) > 0:
        i+=1
    return i+1

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        elves = set()
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == '#':
                    elves.add((x, y))
        p1 = time.time()
        sol1 = part1(set(elves))
        p2 = time.time()
        sol2 = part2(set(elves))
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
