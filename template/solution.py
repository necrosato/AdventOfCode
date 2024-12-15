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

def vector_add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def int_grid(lines):
    return [list(map(int, line.split())) for line in lines]

def coordinate_list(grid):
    return [(i, j, grid[i][j]) for i in range(len(grid)) for j in range(len(grid[i]))]
 
def transpose(grid):
    return list(map(list, zip(*grid)))

def true_func(val):
    return True

def get_neighbors(grid, row, col):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for pair in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i = row+pair[0]
        j = col+pair[1]
        if 0 <= i < rows and 0 <= j < cols:
            neighbors.append(grid[i][j])
    return neighbors

def get_neighbors2(grid, row, col, range_val=1, diagonals=False, include_value=True, value_condition=lambda x:True):
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

def bfs_grid(grid, row, col):
    visited = set()
    order = []
    queue = deque([(row, col, grid[row][col])])
    result = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            result.append(node)
            queue.extend(get_neighbors(grid, node[0], node[1]))
    return result, order

def dfs_grid(grid, row, col, visited=None, order=None):
    if visited==None:
        visited=set()
    if order==None:
        order=[]
    node = (row, col, grid[row][col])
    visited.add(node)
    order.append(node)
    for neighbor in get_neighbors(grid, row, col):
        if neighbor not in visited:
            dfs_grid(grid, neighbor[0], neighbor[1], visited, order)
    return visited, order

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                return (i, j, val)

def grid_find_all(grid, val):
    vals = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                vals.append((i, j, val))
    return vals

def dijkstra_grid(grid, start_val):
    start = grid_find(grid, start_val) 
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
def part1( grid ):
    pass

@timer_func
def part2( grid ):
    pass

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = lines
            sol1 = part1(grid)
            sol2 = part2(grid)
            for timing in list(reversed(sorted(timings, key=lambda x:x[1]))):
                print('function {} took {} seconds total'.format(timing, timings[timing]))
         
if __name__=='__main__':
    main()

