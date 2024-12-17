import argparse
import time
from collections import deque
import heapq

'''
some generic helper functions
'''
def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s returned {result}')
        return result
    return wrap_func

dirs =[(-1, 0),(0, 1),(1, 0),(0, -1)]
def coordinate_list(grid, consec):
    return [(i, j, grid[i][j], d, m) for i in range(len(grid)) for j in range(len(grid[i])) for d in dirs for m in range(consec+1)]
 
def get_neighbors(grid, row, col, d, consec, window):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    rows, cols = range(len(grid)), range(len(grid[0]))
    for nd in dirs:
        i = row+nd[0]
        j = col+nd[1]
        if nd != (-d[0],-d[1]) and i in rows and j in cols:
            if nd == d and consec < window[1]:
                neighbors.append((i,j,grid[i][j], nd, consec+1))
            if nd != d and consec >= window[0]:
                neighbors.append((i,j,grid[i][j], nd, 1))
    return neighbors

def dijkstra_grid(grid, starts, window):
    distances = {node: float('inf') for node in coordinate_list(grid, window[1])}
    for start in starts:
        distances[start] = 0
    visited = set()
    pq = [(0, start) for start in starts]
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)
        row, col, val, d, consec = current_node
        for neighbor in get_neighbors(grid, row, col, d, consec, window):
            distance = current_distance + neighbor[2]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def part( grid, window ):
    starts = [(0, 0, grid[0][0], (0, 1), 0),
              (0, 0, grid[0][0], (1, 0), 0)]
    end = (len(grid)-1, len(grid[0])-1, grid[-1][-1])
    results = dijkstra_grid(grid, starts, window)
    ends = set()
    for r in results:
        if r[0:3] == end:
            ends.add(results[r])
    return min(ends)

@timer_func
def part1(grid):
    return part(grid, (0, 3))

@timer_func
def part2( grid ):
    return part(grid, (4, 10))

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = [list(map(int, list(line))) for line in lines]
            sol1 = part1(grid)
            sol2 = part2(grid)
         
if __name__=='__main__':
    main()
