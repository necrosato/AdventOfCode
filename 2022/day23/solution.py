import time
import sys

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
    xmin = min([elf[0] for elf in elves])
    ymin = min([elf[1] for elf in elves])
    xmax = max([elf[0] for elf in elves])
    ymax = max([elf[1] for elf in elves])
    return (1 + xmax - xmin, 1 + ymax - ymin)

def printElves(elves):
    tx, ty = getDimensions(elves)
    xmin = min([elf[0] for elf in elves])
    ymin = min([elf[1] for elf in elves])
    grid = [['.' for j in range(tx)] for i in range(ty)]
    for elf in elves:
        grid[elf[1]-ymin][elf[0]-xmin] = '#'
    for g in grid:
        print(''.join(g))
 
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
    directions = 'NSWE'
    i = 0
    while i < 10:
        i += 1
        executeRound(elves, directions)
        directions = directions[1:] + directions[0]
    tx, ty = getDimensions(elves)
    return tx*ty - len(elves)

def part2( elves ):
    directions = 'NSWE'
    movements = 1
    i = 0
    while movements > 0:
        i += 1
        movements = executeRound(elves, directions)
        directions = directions[1:] + directions[0]
    return i

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
