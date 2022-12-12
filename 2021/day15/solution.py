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

for fname in ['input.txt', 'input2.txt', 'input3.txt']:
    grid = []
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for line in lines:
            grid.append([int(c) for c in line])
        visited = set()
        heap = [(0, len(grid)-1, len(grid[0])-1)]
        while type(heap) is not int:
            heap = dijkstra(grid, heap, (0, 0), visited)

        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, heap, end-start))
