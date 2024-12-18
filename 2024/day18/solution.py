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

def get_neighbors(grid, row, col, value_condition=lambda x:True):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for pair in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i = row+pair[0]
        j = col+pair[1]
        if 0 <= i < rows and 0 <= j < cols and value_condition(grid[i][j]):
            neighbors.append((i, j, grid[i][j]))
    return neighbors

def coordinate_list(grid):
    return [(i, j, grid[i][j]) for i in range(len(grid)) for j in range(len(grid[i]))]
 
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
def part1( falling, grid ):
    for x, y in falling[:1024]:
        grid[y][x] = '#'
    return dijkstra_grid(grid, (0, 0, '.'))[(len(grid)-1, len(grid)-1, '.')]

@timer_func
def part2( falling, grid ):
    for x, y in falling:
        grid[y][x] = '#'
    for x, y in list(reversed(falling)):
        grid[y][x] = '.'
        if dijkstra_grid(grid, (0, 0, '.'))[(len(grid)-1, len(grid)-1, '.')] != float('inf'):
            return (x,y)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            falling = [tuple(map(int, l.strip().split(','))) for l in f.readlines()]
            grid=[['.']*71 for k in range(71)]
            sol1 = part1(falling, grid)
            sol2 = part2(falling, grid)
         
if __name__=='__main__':
    main()

