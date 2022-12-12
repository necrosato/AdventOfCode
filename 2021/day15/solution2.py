import time
import copy
import heapq

def getAdjacent(i, j, maxi, maxj):
    adjacent = []
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if x <= maxi and x >= 0 and y <= maxj and y >= 0:
            adjacent.append((x, y))
    return adjacent

def dijkstra( grid, heap, end, visited ):
    dist, i, j = heapq.heappop(heap)
    for x, y in getAdjacent(i, j, len(grid)-1, len(grid[0])-1):
        if (x, y) not in visited:
            nd = grid[x][y] + dist
            visited.add((x, y))
            heapq.heappush(heap, (nd, x, y))
    if i != end[0] or j != end[1]:
        return heap
    return dist + grid[-1][-1] - grid[0][0]

def increment(l):
    ret = [e+1 for e in l] 
    for i in range(len(ret)):
        if ret[i] == 10:
            ret[i] = 1
    return ret

for fname in ['input.txt', 'input2.txt', 'input3.txt']:
    grid = []
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for line in lines:
            tmp = [int(c) for c in line]
            row = tmp
            for i in range(4):
                row = increment(row)
                tmp += row
            grid.append(tmp)
        prelen = len(grid)
        for m in range(4):
            for i in range(prelen):
                grid.append(increment(grid[i+prelen*m]))
        visited = set()
        heap = [(0, len(grid)-1, len(grid[0])-1)]
        i = 0
        while type(heap) is not int:
            i+=1
            heap = dijkstra(grid, heap, (0, 0), visited)
        print('{} iterations'.format(i))

        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, heap, end-start))
