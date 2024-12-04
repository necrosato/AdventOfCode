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

'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

def rdiagonal_coords(i, j, h, l):
    if i+3 < h and j+3 < l:
        return [(i, j),(i+1, j+1), (i+2,j+2), (i+3,j+3)]
    return []
def ldiagonal_coords(i, j, h, l):
    if i+3 < h and j-3 >= 0:
        return [(i, j),(i+1, j-1), (i+2,j-2), (i+3,j-3)]
    return []
@timer_func
def part1( grid ):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if j<len(grid[0])-3:
                hword = grid[i][j:j+4]
                if hword in ['XMAS','SAMX']: 
                    total+=1
            if i<len(grid)-3:
                vword = ''.join([grid[i][j],grid[i+1][j],grid[i+2][j],grid[i+3][j]])
                if vword in ['XMAS','SAMX']: 
                    total+=1
            ldcoords = ldiagonal_coords(i, j, len(grid), len(grid[0]))
            if len(ldcoords) == 4:
                ldword = ''.join([grid[ldcoord[0]][ldcoord[1]] for ldcoord in ldcoords])
                if ldword in ['XMAS','SAMX']: 
                    total+=1
            rdcoords = rdiagonal_coords(i, j, len(grid), len(grid[0]))
            if len(rdcoords) == 4:
                rdword = ''.join([grid[rdcoord[0]][rdcoord[1]] for rdcoord in rdcoords])
                if rdword in ['XMAS','SAMX']: 
                    total+=1
    return total 

@timer_func
def part2( grid ):
    total = 0
    for i in range(len(grid)-2):
        for j in range(len(grid[0])-2):
            x = [grid[i][j:j+3],grid[i+1][j:j+3],grid[i+2][j:j+3]]
            diags = [x[0][0]+x[1][1]+x[2][2],x[2][0]+x[1][1]+x[0][2]]
            if diags[0] in ['MAS', 'SAM'] and diags[1] in ['MAS', 'SAM']:
                total += 1
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            grid = lines
            sol1 = part1(grid)
            sol2 = part2(grid)
        
if __name__=='__main__':
    main()

