import time
import sys

def part1( exclusions, y, beacons, minv=None, maxv=None ):
    ranges = set()
    for e in exclusions:
        e.addRowRange(y, ranges, minv, maxv)
    ranges = list(sorted(ranges, key=lambda x: x[0]))
    i = 0
    while i < len(ranges)-1:
        if ranges[i][1] >= ranges[i+1][0]:
            ranges[i] = ((ranges[i][0], max(ranges[i][1], ranges[i+1][1])))
            ranges.pop(i+1)
        else:
            i+=1
    return sum([r[1]-r[0]+1 for r in ranges]) - (0 if y not in beacons else len(beacons[y]))

def part2( exclusions, maxxy, beacons ):
    for y in range(maxxy):
        impossible = part1(exclusions, y, set(), 0, maxxy)
        if maxxy - impossible == 0:
            print('found row y = {} with one free spot'.format(y))
            for x in range(maxxy):
                found = True
                for e in exclusions:
                    if not e.excludes(x, y):
                        found = False
                        break
                if found:
                    print('found col x = {} with one free spot'.format(x))
                    return (x*4000000)+y

class ExclusionZone:
    def __init__(self, sx, sy, bx, by):
        self.sx = sx
        self.sy = sy
        self.bx = bx
        self.by = by
        self.m = abs(sx-bx) + abs(sy-by)
    def addRowRange(self, y, ranges, minx, maxx):
        yoffset = abs(y - self.sy)
        if yoffset <= self.m:
            width = (self.m - yoffset) 
            x1 = self.sx - width
            if minx is not None and x1 < minx:
                x1 = minx
            x2 = self.sx + width
            if maxx is not None and x2 > maxx:
                x2 = maxx
            ranges.add((x1, x2))
    def excludes(self, x, y):
        return abs(x - self.sx) + abs(y - self.sy) > self.m

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip()[10:] for l in f.readlines()]
        beacons = {}
        exclusions = []
        for line in lines:
            sensor, beacon = line.split(': closest beacon is at ')
            sensor = [int(p.split('=')[-1]) for p in sensor.split(', ')]
            beacon = [int(p.split('=')[-1]) for p in beacon.split(', ')]
            if beacon[1] not in beacons:
                beacons[beacon[1]] = set()
            beacons[beacon[1]].add(beacon[0])
            exclusions.append(ExclusionZone(sensor[0], sensor[1], beacon[0], beacon[1]))
        p1 = time.time()
        sol1 = part1(exclusions, 2000000, beacons)
        p2 = time.time()
        sol2 = part2(exclusions, 4000000, beacons)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
