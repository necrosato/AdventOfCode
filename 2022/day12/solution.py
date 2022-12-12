import time
import copy
import heapq

def charHeight(c):
    if c == 'S':
        return 0
    if c == 'E':
        return 27
    return ord(c) - 96

def getAdjacent(i, j, grid):
    adjacent = []
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if x < len(grid) and x >= 0 and y < len(grid[0]) and y >= 0:
            if (grid[x][y] - grid[i][j]) < 2:
                adjacent.append((x, y))
    return adjacent

def dijkstra( grid, heap, end, visited ):
    dist, i, j = heapq.heappop(heap)
    for x, y in getAdjacent(i, j, grid):
        if (x, y) not in visited:
            nd = 1 + dist
            visited.add((x, y))
            heapq.heappush(heap, (nd, x, y))
    if (i, j) != end:
        return heap
    return dist

for fname in ['input.txt', 'input2.txt']:
    grid = []
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for line in lines:
            grid.append([charHeight(c) for c in line])
        end = (0, 0)
        begins = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 27:
                    grid[i][j] = 26
                    end = (i, j)
                if grid[i][j] == 0 or grid[i][j] == 1: ## make second 1 a 0 for part1
                    grid[i][j] = 1
                    begins.append( (i, j) )
        pathlens = []
        for begin in begins:
            visited = set()
            heap = [(0, begin[0], begin[1])]
            while type(heap) is not int and len(heap) > 0:
                heap = dijkstra(grid, heap, end, visited)
            if type(heap) is int:
                pathlens.append(heap)
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, min(pathlens), end-start))
