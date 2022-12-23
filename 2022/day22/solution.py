import time
import sys

xmods = { 0: 1, 90: 0, 180: -1, 270: 0 }
ymods = { 0: 0, 90: 1, 180: 0, 270: -1 }

def parseMoves(path):
    moves = []
    i = 0
    num = True 
    for j in range(len(path)+1):
        if ( num and ( j == len(path) or not path[j].isnumeric() ) ) or ( not num and ( j == len(path) or path[j].isnumeric() ) ):
            moves.append(path[i:j] if not num else int(path[i:j]))
            i = j
            num = not num
    return moves

def getNextPos(x, y, xmod, ymod, grid):
    nx = x
    ny = y
    nv = ' '
    while nv == ' ':
        nx += xmod
        ny += ymod
        if nx >= len(grid[0]):
            nx = 0
        if nx < 0:
            nx = len(grid[0])-1
        if ny >= len(grid):
            ny = 0
        if ny < 0:
            ny = len(grid)-1
        nv = grid[ny][nx]
    return (nx, ny)

def moveUntilStop(pos, deg, n, grid):
    for i in range(n):
        nx, ny = getNextPos(pos[0], pos[1], xmods[deg], ymods[deg], grid)
        if grid[ny][nx] != '.':
            break
        pos = [nx, ny]
    return pos

def follow(moves, grid):
    pos = [grid[0].index('.'), 0]
    deg = 0
    for move in moves:
        if move == 'L':
            deg = (deg - 90) % 360
        elif move == 'R':
            deg = (deg + 90) % 360
        else:
            pos = moveUntilStop(pos, deg, move, grid)
    return sum([1000*(pos[1]+1), 4*(pos[0]+1), deg//90])

def tile(grid):
    tile_width = int((sum([len(l.strip()) for l in grid]) // 6)**.5)
    tiles = [[[] for col in range(len(grid[0]) // tile_width)] for row in range(len(grid) // tile_width)]
    row = 0
    t = 0
    while t < 6:
        col = len(grid[row]) - len(grid[row].lstrip())
        for i in range(len(grid[row].strip())//tile_width):
            tile = [grid[row+r][col:col+tile_width] for r in range(tile_width)]
            tiles[row // tile_width][col // tile_width] = tile
            col += tile_width
            t+=1
        row += tile_width
    return tiles


for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l for l in f.readlines()]
        grid = [l+' '*(max([len(l)-1 for l in lines[:-2]])-len(l)) for l in [line[:-1] for line in lines[:-2]]]
        moves = parseMoves(lines[-1][:-1])
        p1 = time.time()
        sol1 = follow(moves, grid)
        p2 = time.time()
        tiles = tile(grid)
        print(tiles)
        sol2 = follow(moves, grid)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
