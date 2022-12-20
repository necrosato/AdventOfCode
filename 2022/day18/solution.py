import time
import sys

def getNeighbors(x, y, z):
    return [(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)]
def inRange(x, y, z, xr, yr, zr):
    return not ( x < xr[0] or x > xr[1] or y < yr[0] or y > yr[1] or z<zr[0] or z>zr[1] )

def part1( cubes, xr, yr, zr, exitCoords=None ):
    surface_area = 0
    for x in range(xr[0], xr[1]+1):
        for y in range(yr[0], yr[1]+1):
            for z in range(zr[0], zr[1]+1):
                if (x, y, z) in cubes:
                    for neighbor in getNeighbors(x, y, z):
                        if neighbor not in cubes:
                            if exitCoords is None or neighbor in exitCoords or not inRange(*neighbor, xr, yr, zr):
                                surface_area += 1
    return surface_area

def addExitCoords(x, y, z, xr, yr, zr, exitCoords, cubes):
    tocheck = set([(x, y, z)])
    checked = set()
    while len(tocheck) > 0:
        i, j, k = next(iter(tocheck))
        tocheck.remove((i, j, k))
        if (i, j, k) not in cubes:
            checked.add((i, j, k))
            if ( not inRange(i, j, k, xr, yr, zr) ) or (i, j, k) in exitCoords:
                for coords in tocheck.union(checked):
                    exitCoords.add(coords)
                return
            else:
                for neighbor in getNeighbors(i, j, k):
                    if neighbor not in checked:
                        tocheck.add(neighbor)

def part2( cubes, xr, yr, zr ):
    exitCoords = set()
    for x in range(xr[0], xr[1]+1):
        for y in range(yr[0], yr[1]+1):
            for z in range(zr[0], zr[1]+1):
                addExitCoords(x, y, z, xr, yr, zr, exitCoords, cubes)
    return part1(cubes, xr, yr, zr, exitCoords)

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        xr = [0, 0]
        yr = [0, 0]
        zr = [0, 0]
        cubes = set()
        for line in lines:
            x, y, z = [int(p) for p in line.split(',')]
            xr = [min(xr[0], x), max(xr[1], x)]
            yr = [min(yr[0], y), max(yr[1], y)]
            zr = [min(zr[0], z), max(zr[1], z)]
            cubes.add((x, y, z))
        p1 = time.time()
        sol1 = part1(cubes, xr, yr, zr)
        p2 = time.time()
        sol2 = part2(cubes, xr, yr, zr)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
