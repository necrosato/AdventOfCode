import heapq
import time
import sys

def newSpot(x, y, blizzard, mx, my):
    nx = x+1 if blizzard =='>' else x-1 if blizzard =='<' else x
    ny = y+1 if blizzard =='v' else y-1 if blizzard =='^' else y
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
    options = [(x, y)] if (x, y) not in blizzards else []
    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if (nx, ny) == dst or (0 <= nx <= maxx and 0 <= ny <= maxy and (nx, ny) not in blizzards):
            options.append((nx, ny))
    return options

def dijkstra( heap, dst, visited, maxx, maxy, all_blizzards):
    time, src = heapq.heappop(heap)
    for nd in getOptions(*src, dst, maxx, maxy, all_blizzards[(time+1)%len(all_blizzards)]):
        if (time+1, nd) not in visited:
            visited.add((time+1, nd))
            heapq.heappush(heap, (time+1, nd))
    if src != dst:
        return heap
    return time 

def part1(all_blizzards, src, dst, maxx, maxy, stime=0):
    heap = [(stime, src)]
    visited = set()
    while type(heap) != int:
        heap = dijkstra(heap, dst, visited, maxx, maxy, all_blizzards)
    return heap

def part2(all_blizzards, maxx, maxy, stime=0):
    e2s = part1(all_blizzards, (maxx, maxy+1), (0, -1), maxx, maxy, stime)
    return part1(all_blizzards, (0, -1), (maxx, maxy+1), maxx, maxy, e2s)

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
