import time
import heapq

def charHeight(c):
    if c == 'S':
        return 1
    if c == 'E':
        return 26
    return ord(c) - 96

def getAdjacent(i, j, grid):
    adjacent = []
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if x < len(grid) and x >= 0 and y < len(grid[0]) and y >= 0:
            if (grid[x][y][0] - grid[i][j][0]) < 2:
                adjacent.append((x, y))
    return adjacent
    
def getAdjacentReverse(i, j, grid):
    adjacent = []
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if x < len(grid) and x >= 0 and y < len(grid[0]) and y >= 0:
            if (grid[i][j][0] - grid[x][y][0]) < 2:
                adjacent.append((x, y))
    return adjacent

def dijkstra( grid, heap, val, visited, afunc ):
    dist, i, j = heapq.heappop(heap)
    for x, y in afunc(i, j, grid):
        if (x, y) not in visited:
            nd = 1 + dist
            visited.add((x, y))
            heapq.heappush(heap, (nd, x, y))
    if grid[i][j] != val:
        return heap
    return dist

def steps(src, dst, grid, afunc):
    heap = [(0, src[0], src[1])]
    visited = set()
    while type(heap) is not int and len(heap) > 0:
        heap = dijkstra(grid, heap, dst, visited, afunc)
    return heap

for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        grid = [[(charHeight(c),c) for c in line] for line in lines]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == (1,'S'):
                    src = (i, j)
                if grid[i][j] == (26,'E'):
                    dst = (i, j)
        p1 = time.time()
        sol = steps(src, (26,'E'), grid, getAdjacent)
        p2 = time.time()
        sol = steps(dst, (1, 'a'), grid, getAdjacentReverse)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
