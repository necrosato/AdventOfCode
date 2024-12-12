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
    return [list(map(int, line.split())) for line in lines]

def true_func(region):
    return True

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

def in_region(grid, i, j, val):
    rows, cols = len(grid), len(grid[0])
    if 0 <= i < rows and 0 <= j < cols:
        return grid[i][j] == val
    return False

def get_neighbors2(grid, row, col, range_val=1, diagonals=True, include_value=True, value_condition=lambda x:True):
    """Gets neighboring elements within a given range in a grid."""
    neighbors = []
    val = grid[row][col]
    for i in range(row - range_val, row + range_val + 1):
        for j in range(col - range_val, col + range_val + 1):
            if i != row and j != col:
                n1_in = in_region(grid, row, j, val)
                n2_in = in_region(grid, i, col, val)
                n3_in = in_region(grid, i, j, val)
                if (n1_in and n2_in and not n3_in) or (not n1_in and not n2_in):
                    neighbors.append((i,j)) 
    return neighbors


def fill(grid, i, j, regions, region, seen):
    if (i, j) not in seen:
        seen.add((i, j))
        neighbors = get_neighbors(grid, i, j, value_condition=lambda x:x==grid[i][j])
        sides = 4-len(neighbors)
        regions[region][(i, j)] = sides
        for neighbor in neighbors:
            fill(grid, neighbor[0], neighbor[1], regions, region, seen)

def count_sides(grid, region):
    sides = list()
    for point in region:
        i, j = point
        neighbors = get_neighbors2(grid, i, j, value_condition=lambda x:x!=grid[i][j])
        for neighbor in neighbors:
            sides.append(neighbor)
    return len(sides)
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
    seen = set()
    regions = {}
    price=0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in seen:
                regions[(i, j, grid[i][j])] = {}
                fill(grid, i, j, regions, (i, j, grid[i][j]), seen)
    for region in regions:
        area = len(regions[region])
        perimiter = sum([regions[region][point] for point in regions[region]])
        price += area*perimiter
    return price

@timer_func
def part2( grid ):
    seen = set()
    regions = {}
    price=0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in seen:
                regions[(i, j, grid[i][j])] = {}
                fill(grid, i, j, regions, (i, j, grid[i][j]), seen)
    for region in regions:
        area = len(regions[region])
        sides = count_sides(grid, regions[region])
        price += area*sides
    return price

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            sol1 = part1(lines)
            sol2 = part2(lines)
        
if __name__=='__main__':
    main()

