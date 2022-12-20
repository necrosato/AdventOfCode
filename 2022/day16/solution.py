import itertools
import heapq
import time
import sys
import copy

def maxValveScore(minutes, src, valvemap, valve_distances, unvisited):
    scores = [valvemap[src].rate*(minutes-1)]
    for dst in unvisited:
        uvc = copy.deepcopy(unvisited)
        uvc.remove(dst)
        dt = minutes - valve_distances[src][dst] - ( 1 if valvemap[src].rate > 0 else 0 ) 
        if dt > 0:
            scores.append(maxValveScore(dt, dst, valvemap, valve_distances, uvc) + scores[0])
    return max(scores)

def getNonZeroValves(valvemap):
    unvisited = set()
    for valve in valvemap:
        if valvemap[valve].rate > 0:
            unvisited.add(valve)
    return unvisited

def part1( src, valve_distances, valvemap ):
    return maxValveScore(30, src, valvemap, valve_distances, getNonZeroValves(valvemap))

def part2( src, valve_distances, valvemap ):
    unvisited = getNonZeroValves(valvemap)
    scores = []
    checked = set()
    for i in range(len(unvisited)//2-1,len(unvisited)//2+1):
        for subset in itertools.combinations(unvisited, i):
            comp = tuple(unvisited.difference(subset))
            if subset in checked or comp in checked:
                continue
            checked.add(subset)
            checked.add(comp)
            score = maxValveScore(26, src, valvemap, valve_distances, set(subset))
            score += maxValveScore(26, src, valvemap, valve_distances, set(comp))
            scores.append(score)
    return max(scores)

def dijkstra( heap, dst, visited, valvemap ):
    dist, name = heapq.heappop(heap)
    for tunnel in valvemap[name].tunnels:
        if tunnel not in visited:
            nd = 1 + dist
            visited.add(tunnel)
            heapq.heappush(heap, (nd, tunnel))
    if name != dst:
        return heap
    return dist

class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate 
        self.tunnels = tunnels
    def __repr__(self):
        return '{} {} {}'.format(self.name, self.rate, self.tunnels)
    def getDist(self, otherName, valvemap):
        heap = [(0, self.name)]
        visited = set()
        while type(heap) != int:
            heap = dijkstra(heap, otherName, visited, valvemap)
        return heap

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        valvemap = {}
        for parts in [line.split() for line in lines]:
            valve = Valve(parts[1], int(parts[4].split('=')[-1][:-1]), [part.strip(',') for part in parts[9:]])
            valvemap[valve.name] = valve
        valve_distances = {}
        for src in valvemap:
            distances = {}
            for dst in valvemap:
                distances[dst] = valvemap[src].getDist(dst, valvemap)
            valve_distances[src] = distances
        p1 = time.time()
        sol1 = part1('AA', valve_distances, valvemap)
        p2 = time.time()
        sol2 = part2('AA', valve_distances, valvemap)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
