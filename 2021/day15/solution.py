import time
import copy
import heapq

def getAdjacent(i, j, maxi, maxj):
    adjacent = []
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if x <= maxi and x >= 0 and y <= maxj and y >= 0:
            adjacent.append((x, y))
    return adjacent

def dijkstra( grid, i, j, endi, endj, distances, unvisited ):
    for x, y in getAdjacent(i, j, len(grid)-1, len(grid[0])-1):
        if (x, y) in unvisited:
            dist = grid[x][y] + distances[(i,j)]
            if (x, y) not in distances or distances[(x, y)] > dist:
                distances[(x, y)] = dist
    unvisited.remove((i, j))
    if i != endi or j != endj:
        for pair in list(sorted(distances.items(), key=lambda p: p[1])):
            if pair[0] in unvisited:
                return pair[0]
    return None

for fname in ['input.txt', 'input2.txt', 'input3.txt']:
    solution = 0
    grid = []
    distances = {}
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for line in lines:
            grid.append([int(c) for c in line])
        distances[(len(grid)-1, len(grid[0])-1)] = 0
        unvisited = set()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                unvisited.add((i, j))
        node = (len(grid)-1, len(grid[0])-1)
        while node is not None:
            node = dijkstra(grid, node[0], node[1], 0, 0, distances, unvisited)

        solution = distances[(0,0)] + grid[-1][-1] - grid[0][0]
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, solution, end-start))
