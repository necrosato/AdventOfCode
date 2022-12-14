import time
import sys

class Sand:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def fall(self, world):
        if not world.hasSolid((self.x, self.y+1)):
            self.y += 1
            return True
        elif not world.hasSolid((self.x-1, self.y+1)):
            self.x -= 1
            self.y += 1
            return True
        elif not world.hasSolid((self.x+1, self.y+1)):
            self.x += 1
            self.y += 1
            return True
        return False
    def fallUntilForever(self, world):
        while not ( self.x not in world.maxys or self.y >= world.maxys[self.x] ):
            if not self.fall(world):
                world.sands.add((self.x, self.y))
                return False
        return True
    def fallUntilFloor(self, world):
        while self.fall(world):
            pass
        world.sands.add((self.x, self.y))
        return True

class World:
    def __init__(self, rocks, maxys, floor=-1):
        self.rocks = rocks
        self.sands = set()
        self.maxys = maxys
        self.floor = floor
    def hasSolid(self, coords):
        if coords in self.rocks:
            return True
        if coords in self.sands:
            return True
        if self.floor > 0 and self.floor - coords[1] == 0:
            return True
        return False

def part1(world, source):
    sol = 0
    while True:
        sand = Sand(source[0], source[1])
        if sand.fallUntilForever(world):
            break
        sol += 1
    return sol

def part2(world, source):
    sol = 0
    while source not in world.sands:
        sand = Sand(source[0], source[1])
        sand.fallUntilFloor(world)
        sol += 1
    return sol

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        rocks = set()
        maxys = {}
        maxy = 0
        for line in lines:
            points = line.split(' -> ')
            for i in range(len(points)-1):
                p1 = [int(n)for n in points[i].split(',')]
                p2 = [int(n)for n in points[i+1].split(',')]
                for rock in [(x+min(p1[0], p2[0]), y+min(p1[1], p2[1])) for x in range(abs(p1[0] - p2[0])+1) for y in range(abs(p1[1] - p2[1])+1)]:
                    rocks.add(rock)
                    maxy = max(rock[1], maxy)
                    if rock[0] not in maxys:
                        maxys[rock[0]] = rock[1]
                    maxys[rock[0]] = max(maxys[rock[0]], rock[1])
        maxy += 2
        source = (500, 0)
        p1 = time.time()
        sol1 = part1(World(rocks, maxys), source)
        p2 = time.time()
        sol2 = part2(World(rocks, maxys, maxy), source)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
