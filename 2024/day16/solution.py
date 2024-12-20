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

timings = {}
def instrument(silent=False):
    def decorator(func):
        def wrap_func(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            duration = t2-t1
            if not silent:
                print(f'Function {func.__name__!r} executed in {(duration):.4f}s returned {result}')
            if func.__name__ not in timings:
                timings[func.__name__] = 0
            timings[func.__name__] += duration 
            return result
        return wrap_func
    return decorator

dirs =[(-1, 0),(0, 1),(1, 0),(0, -1)]
def coordinate_list(grid):
    return [(i, j, grid[i][j], d) for i in range(len(grid)) for j in range(len(grid[i])) for d in dirs]
 
def get_neighbors(grid, row, col, d, range_val=1, diagonals=False, include_value=True, value_condition=lambda x:True):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for i in range(row - range_val, row + range_val + 1):
        for j in range(col - range_val, col + range_val + 1):
            if 0 <= i < rows and 0 <= j < cols and (i != row or j != col):
                if diagonals or i == row or j == col:
                    if value_condition(grid[i][j]):
                        nd = (i-row, j-col)
                        cost = 1 if nd == d else 1001
                        neighbors.append((i,j,grid[i][j], nd, cost) if include_value else (i,j, nd, cost)) 
    return neighbors

def get_neighbors2(grid, row, col, d, value_condition=lambda x:True):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    i = row-d[0]
    j = col-d[1]
    if value_condition(grid[i][j]):
        for d2 in dirs:
            cost = 1 if d2 == d else 1001
            neighbors.append((i,j,grid[i][j], d2, cost)) 
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
        if current_node in visited:
            continue
        visited.add(current_node)
        row, col, val, d = current_node
        for neighbor in get_neighbors(grid, row, col, d, value_condition=lambda x:x!='#'):
            distance = current_distance + neighbor[-1]
            if distance < distances[neighbor[:-1]]:
                distances[neighbor[:-1]] = distance
                heapq.heappush(pq, (distance, neighbor[:-1]))
    return distances

def dijkstra_grid2(grid, start):
    distances = {node: float('inf') for node in coordinate_list(grid)}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)
        row, col, val, d = current_node
        for neighbor in get_neighbors2(grid, row, col, d, value_condition=lambda x:x!='#'):
            distance = current_distance + neighbor[-1]
            if distance < distances[neighbor[:-1]]:
                distances[neighbor[:-1]] = distance
                heapq.heappush(pq, (distance, neighbor[:-1]))
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
def part1( grid ):
    start = (*grid_find(grid, 'S'), (0, 1))
    results = dijkstra_grid(grid, start)
    ends = {}
    for r in results:
        if r[2] == 'E':
            ends[r] = results[r]
    return min(ends.values()) 

def best_result(results_map, ijcd):
    res = set()
    for r in results_map:
        res.add(results_map[r][ijcd])
    return min(res)
 
@timer_func
def part2( grid ):
    start = (*grid_find(grid, 'S'), (0, 1))
    results = dijkstra_grid(grid, start)
    ends = {}
    for r in results:
        if r[2] == 'E':
            ends[r] = results[r]
    best_len = min(ends.values()) 
    end_results = {}
    for e in ends:
        end_results[e] = dijkstra_grid2(grid, e)
    bps = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            c = grid[i][j]
            for d in dirs:
                ijcd = (i, j, c, d)
                if best_len == results[ijcd] + best_result(end_results, ijcd):
                    bps.add((i, j))
    return len(bps)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = [list(l.strip()) for l in f.readlines()]
            sol1 = part1(grid)
            sol2 = part2(grid)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

