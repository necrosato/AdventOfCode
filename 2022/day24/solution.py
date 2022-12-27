import heapq
import time
import sys

def newSpot(x, y, blizzard, mx, my):
    nx = x
    ny = y
    if blizzard == '>':
        nx += 1
    if blizzard == '<':
        nx -= 1
    if blizzard == '^':
        ny -= 1
    if blizzard == 'v':
        ny += 1
    return (nx%(mx+1), ny%(my+1))

def moveBlizzards(blizzards, maxx, maxy):
    new = {}
    for spot in blizzards:
        for blizzard in blizzards[spot]:
            ns = newSpot(*spot, blizzard, maxx, maxy)
            if ns not in new:
                new[ns] = []
            new[ns].append(blizzard)
    return new

def getOptions(x, y, dst, maxx, maxy, blizzards):
    options = []
    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x, y)]:
        if (nx, ny) == dst or ((nx, ny) == (x, y) and (x, y) not in blizzards) or (0 <= nx <= maxx and 0 <= ny <= maxy and (nx, ny) not in blizzards):
            options.append((nx, ny))
    return options

def dijkstra( heap, dst, visited, maxx, maxy, all_blizzards):
    time, src = heapq.heappop(heap)
    nt = time+1
    for nd in getOptions(*src, dst, maxx, maxy, all_blizzards[(nt)%len(all_blizzards)]):
        if (nd, nt) not in visited:
            visited.add((nd, nt))
            heapq.heappush(heap, (nt, nd))
    if src != dst:
        return heap
    print("dijkstra stopping at {}, {} minutes".format(src, time))
    return time 

def part1(all_blizzards, src, dst, maxx, maxy, stime=0):
    heap = [(stime, src)]
    visited = set()
    while type(heap) != int:
        heap = dijkstra(heap, dst, visited, maxx, maxy, all_blizzards)
    print('{} to {}: {} minutes'.format(src, dst, heap))
    return heap

def part2(all_blizzards, maxx, maxy, stime=0):
    e2s = part1(all_blizzards, (maxx, maxy+1), (0, -1), maxx, maxy, stime)
    print('Part2 going from end to start took {} ( {} - {} ) minutes'.format(e2s-stime, e2s, stime))
    s2e = part1(all_blizzards, (0, -1), (maxx, maxy+1), maxx, maxy, e2s)
    print('Part2 going from start back to end took {} ( {} - {} ) minutes'.format(s2e-e2s, s2e, e2s))
    return s2e

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        blizzards = {}
        maxx, maxy = (len(lines[0])-3, len(lines)-3)
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] != '#' and lines[y][x] != '.':
                    blizzards[(x-1, y-1)] = [lines[y][x]]
        all_blizzards = [blizzards]
        bs = moveBlizzards(blizzards, maxx, maxy)
        while bs != blizzards:
            all_blizzards.append(bs)
            bs = moveBlizzards(bs, maxx, maxy)

        p1 = time.time()
        sol1 = part1(all_blizzards, (0, -1), (maxx, maxy+1), maxx, maxy)
        p2 = time.time()
        sol2 = part2(all_blizzards, maxx, maxy, sol1)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
