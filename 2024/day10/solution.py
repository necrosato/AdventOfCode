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

def int_grid(lines):
    return [list(map(int, list(line.split()[0]))) for line in lines]

def coordinate_list(grid):
    return [(i, j, grid[i][j]) for i in range(len(grid)) for j in range(len(grid[i]))]
 
def get_neighbors(grid, row, col, range_val=1, diagonals=False, include_value=True):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for i in range(row - range_val, row + range_val + 1):
        for j in range(col - range_val, col + range_val + 1):
            if 0 <= i < rows and 0 <= j < cols and (i != row or j != col):
                if diagonals or i == row or j == col:
                    if ((grid[i][j]-grid[row][col])==1):
                        neighbors.append((i,j,grid[i][j]) if include_value else (i,j)) 
    return neighbors

def dijkstra_grid(grid, start):
    distances = {node: float('inf') for node in coordinate_list(grid)}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)
        row, col, val = current_node
        for neighbor in get_neighbors(grid, row, col, diagonals=False):
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

def find_all(grid, val):
    vals = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == val:
                vals.append((i, j, val))
    return vals

badmemo = set()
def distinct_paths(grid, start, finish):
    new = []
    if (start, finish) not in badmemo:
        for neighbor in get_neighbors(grid, start[0], start[1]):
            if neighbor != finish:
                new+=distinct_paths(grid, neighbor, finish)
            else:
                new.append([finish])
    if new == []:
        badmemo.add((start, finish))
    return [[start]+path for path in new]

'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

@timer_func
def part1( grid ):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                distances = dijkstra_grid(grid, (i, j, grid[i][j]))
                for node in distances:
                    if node[-1] == 9 and distances[node] != float('inf'):
                        total += 1
    return total

@timer_func
def part2( grid ):
    total = 0
    starts = find_all(grid, 0)
    ends = find_all(grid, 9)
    for start in starts:
        for end in ends:
            paths = distinct_paths(grid, start, end)
            total += len(paths)
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = int_grid(lines)
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

