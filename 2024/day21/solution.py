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

def vector_sub(v1, v2):
    return tuple(y - x for x, y in zip(v1, v2))

def maybe_int(n):
    try:
        return int(n)
    except:
        return n
    
def int_grid(lines):
    return [list(map(maybe_int, list(line))) for line in lines]

def get_neighbors(grid, row, col):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for pair in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i = row+pair[0]
        j = col+pair[1]
        if 0 <= i < rows and 0 <= j < cols and grid[i][j] != None:
            neighbors.append(grid[i][j])
    return neighbors

def grid_find(grid, val):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val:
                return (i, j)

def grid_to_graph(grid):
    graph = {}
    for i,row in enumerate(grid):
        for j,val in enumerate(row):
            if val is not None:
                graph[val] = []
                for neighbor in get_neighbors(grid, i, j):
                    graph[val].append((neighbor, 1))
    return graph

dirs = {(0,1):'>',(0,-1):'<',(-1,0):'^',(1,0):'v'}
def floyd_warshall_all_paths(grid):
    graph = grid_to_graph(grid)
    # Initialize the distance and paths matrices
    nodes = list(graph.keys())
    dist = {node: {other: float('inf') for other in nodes} for node in nodes}
    paths = {node: {other: [] for other in nodes} for node in nodes}
    
    # Initialize the distance matrix and path matrix with direct edges
    for node in nodes:
        dist[node][node] = 0
        paths[node][node] = [[node]]  # A path from a node to itself is just the node itself
        for neighbor, weight in graph[node]:
            dist[node][neighbor] = weight
            paths[node][neighbor] = [[node, neighbor]]
    
    # Floyd-Warshall algorithm to update shortest paths
    for k in nodes:
        for i in nodes:
            for j in nodes:
                # If we find a shorter path through node k
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    paths [i][j] = []
                    for ep in paths[k][j]:
                        paths[i][j] += [path + ep[1:] for path in paths[i][k]]  # All paths from i to j via k
                # If we find another path of the same length, we add it
                elif dist[i][j] == dist[i][k] + dist[k][j] and i != k and j != k:
                    for ep in paths[k][j]:
                        paths[i][j] += [path + ep[1:] for path in paths[i][k]]  # All paths from i to j via k
    
    dirpaths = {node: {other: [] for other in nodes} for node in nodes}
    for i in paths:
        for j in paths[i]:
            for path in paths[i][j]:
                pd = []
                for p in range(len(path)-1):
                    d = vector_sub(grid_find(grid, path[p]),grid_find(grid, path[p+1]))
                    pd.append(dirs[d])
                pd.append('A')
                dirpaths[i][j].append(pd)
    return dist, paths, dirpaths

'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

numpad = [
        [7,8,9],
        [4,5,6],
        [1,2,3],
        [None,0,'A']
        ]
dpad = [
        [None,'^','A'],
        ['<','v','>']
        ]

class Keypad:
    def __init__(self, grid):
        self.grid = grid
        self.dists, self.paths, self.dirpaths = floyd_warshall_all_paths(grid)

memo = {}
def minimum_path_length(i, code, keypads):
    if i == len(keypads)-1:
        return len(code)
    keypad = keypads[i]
    total = 0
    memokey = (i, ''.join(map(str,code)), len(keypads))
    if memokey in memo:
        return memo[memokey]
    for start, end in zip(['A']+code, code):
        lens = [minimum_path_length(i+1, path, keypads) for path in keypad.dirpaths[start][end]]
        total += 1 if not lens else min(lens)
    memo[memokey] = total
    return total

def complexity(dpad_num, grid):
    keypads = [Keypad(numpad)]
    for i in range(dpad_num):
        keypads.append(Keypad(dpad))
    return sum([minimum_path_length(0, code, keypads)*int(''.join(map(str,code[:-1]))) for code in grid])

@timer_func
def part1( grid ):
    return complexity(3,grid)

@timer_func
def part2( grid ):
    return complexity(26,grid)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            grid = int_grid([l.strip() for l in f.readlines()])
            sol1 = part1(grid)
            sol2 = part2(grid)
         
if __name__=='__main__':
    main()

