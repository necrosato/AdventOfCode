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

def coordinate_list(grid):
    return [(i, j, grid[i][j]) for i in range(len(grid)) for j in range(len(grid[i]))]
 
def get_neighbors(grid, row, col, range_val=1, diagonals=False, include_value=True, value_condition=lambda x:True):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for i in range(row - range_val, row + range_val + 1):
        for j in range(col - range_val, col + range_val + 1):
            if 0 <= i < rows and 0 <= j < cols and (i != row or j != col):
                if diagonals or i == row or j == col:
                    if value_condition(grid[i][j]):
                        neighbors.append((i,j,grid[i][j]) if include_value else (i,j)) 
    return neighbors

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                return (i, j, val)

def dijkstra_grid(grid, start):
    distances = {node: float('inf') for node in coordinate_list(grid)}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node not in visited:
            visited.add(current_node)
            row, col, val = current_node
            for neighbor in get_neighbors(grid, row, col, value_condition=lambda x:x!='#'):
                distance = current_distance + 1
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

@timer_func
def solve(grid, cheatlen, minsave):
    start = grid_find(grid, 'S') 
    end = grid_find(grid, 'E') 
    results = dijkstra_grid(grid, start)
    from_end = dijkstra_grid(grid, end)
    total = 0
    for node in results:
        dist = results[node]
        if dist != float('inf'):
            for i in range(-cheatlen, cheatlen+1):
                i2 = i + node[0]
                for j in range(-(cheatlen-abs(i)), cheatlen-abs(i)+1):
                    j2 = j + node[1]
                    distance = abs(i) + abs(j)
                    if distance > 1 and i2 >=0 and i2 < len(grid) and j2 >=0 and j2<len(grid[0]):
                        total += results[end]-((dist + from_end[(i2, j2, grid[i2][j2])])+distance) >= minsave
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [list(l.strip()) for l in f.readlines()]
            solve(grid, 2, 100)
            solve(grid, 20, 100)
         
if __name__=='__main__':
    main()
