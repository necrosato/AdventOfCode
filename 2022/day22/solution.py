import time
import sys
from matplotlib import pyplot as plt

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

# cube moves around the player so player is always on top
def moveUntilStop3d(pos, g2c, n, grid, visited):
    width = int((sum([len(l.strip()) for l in grid]) // 6)**.5)
    pos3d = g2c[pos]
    c2g = cubeToGrid(g2c)
    tmp = g2c
    for i in range(n):
        x, y, z = pos3d 
        if (x+1, y, z) in c2g:
            pos3d = (x+1, y, z)
        else:
            pos3d = (1, y, z)
            tmp = rotateY(g2c, width, -1)
            c2g = cubeToGrid(tmp)
            #plot(g2c, visited)
        j, i = c2g[pos3d] 
        if grid[i][j] != '.':
            break
        g2c = tmp
        pos = (j, i)
        visited.append(pos)
    #plot(g2c, visited)
    return (pos, g2c)

def follow3d(moves, grid):
    width = int((sum([len(l.strip()) for l in grid]) // 6)**.5)
    vstart = grid[0].index('.')
    visited = [(vstart, 0)]
    #visited = [(j, i) for i in range(0, width//2) for j in range(vstart, vstart+width)]
    g2c = gridToCube(grid, width, visited)
    pos = visited[0]
    pos3d = g2c[visited[0]]
    for i in range(len(moves)):
        move = moves[i]
        print('move {} / {} - {}'.format(i+1, len(moves), move))
        if move == 'L':
            g2c = rotateZ(g2c, width, -1)
            #plot(g2c, visited)
        elif move == 'R':
            g2c = rotateZ(g2c, width, 1)
            #plot(g2c, visited)
        else:
            pos, g2c = moveUntilStop3d(pos, g2c, move, grid, visited)
    print(visited[-2:])
    print([1000*(pos[1]+1), 4*(pos[0]+1)])
    return sum([1000*(pos[1]+1), 4*(pos[0]+1)])



def coordMap3d(grid):
    cm3d = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != ' ':
                cm3d[(j, i)] = (j, i, 0) 
    return cm3d

def gridToCube(grid, width, visited):
    g2c = coordMap3d(grid)
    plot(g2c, visited)
    '''
    #for input2
    g2c = foldY(g2c, width, -1, -1)
    plot(g2c, visited)
    g2c = foldY(g2c, width*2, -1, -1)
    plot(g2c, visited)
    g2c = foldY(g2c, width*3-1, -1, 1)
    plot(g2c, visited)
    g2c = foldX(g2c, width, -1, -1)
    plot(g2c, visited)
    g2c = foldX(g2c, width*2-1, -1, 1)
    plot(g2c, visited)
    g2c = rotateX(fixCoords(g2c), width)
    '''
    #for input
    g2c = foldY(g2c, width*2-1, -1, 1)
    g2c = foldX(g2c, width, -1, -1)
    g2c = foldX(g2c, width*2, -1, -1)
    g2c = foldX(g2c, width*3-1, -1, 1)
    g2c = foldY(g2c, width-1, -1, 1)
    g2c = rotateY(fixCoords(g2c), width)
    g2c = rotateZ(fixCoords(g2c), width)
    g2c = rotateZ(fixCoords(g2c), width)
    plot(g2c, visited)
    return fixCoords(g2c)

def cubeToGrid(gridToCube):
    return { gridToCube[coords]:coords for coords in gridToCube } 


def fixCoords(g2c):
    new = {}
    minx, maxx = (min([g2c[e][0] for e in g2c]), max([g2c[e][0] for e in g2c]))
    miny, maxy = (min([g2c[e][1] for e in g2c]), max([g2c[e][1] for e in g2c]))
    minz, maxz = (min([g2c[e][2] for e in g2c]), max([g2c[e][2] for e in g2c]))
    for i, j in g2c:
        x, y, z = g2c[(i, j)]
        nx = x - minx
        ny = y - miny
        nz = z - minz
        new[(i, j)] = (nx, ny, nz)
    return new

def foldX(g2c, axis, direction=1, side=-1):
    #print('Fold x axis along y={}'.format(axis))
    new = {}
    for i, j in g2c:
        x, y, z = g2c[(i, j)]
        operate = y < axis if side == -1 else y > axis
        nx = x
        ny = (axis+side) + z*side*direction if operate else y
        nz = side*direction*(axis-y) if operate else z
        if (nx, ny, nz) in new:
            print('{} colliding into a spot'.format((nx, ny, nz)))
        new[(i, j)] = (nx, ny, nz)
    return new
def foldY(g2c, axis, direction=1, side=-1):
    #print('Fold y axis along x={}'.format(axis))
    new = {}
    for i, j in g2c:
        x, y, z = g2c[(i, j)]
        operate = x < axis if side == -1 else x > axis
        nx = (axis+side) + z*side*direction if operate else x
        ny = y
        nz = side*direction*(axis-x) if operate else z
        if (nx, ny, nz) in new:
            print('{} colliding into a spot'.format((nx, ny, nz)))
        new[(i, j)] = (nx, ny, nz)
    return new

def rotateZ(g2c, width, direction=1):
    #print('rotating on z axis direction ' + str(direction))
    new = rotateX(g2c, width+2, -1)
    new = rotateY(new, width+2, direction)
    new = rotateX(new, width+2, 1)
    return new
def rotateY(g2c, width, direction=1):
    #print('rotating on y axis direction ' + str(direction))
    new = {}
    if direction == 1:
        new = foldY(g2c, width+2+1)
    else:
        new = foldY(g2c, -1, 1, 1)
    return fixCoords(new)
def rotateX(g2c, width, direction=1):
    #print('rotating on x axis direction ' + str(direction))
    new = {}
    if direction == 1:
        new = foldX(g2c, width+2+1)
    else:
        new = foldX(g2c, -1, 1, 1)
    return fixCoords(new)
 
def plot(g2c, visited=[]):
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    x, y, z = zip(*[g2c[coords] for coords in g2c])
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(x, y, z)
    if len(visited) > 0:
        x, y, z = zip(*[g2c[coords] for coords in visited])
        ax.scatter(x, y, z, color='red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l for l in f.readlines()]
        grid = [l+' '*(max([len(l)-1 for l in lines[:-2]])-len(l)) for l in [line[:-1] for line in lines[:-2]]]
        moves = parseMoves(lines[-1][:-1])
        p1 = time.time()
        sol1 = follow(moves, grid)
        p2 = time.time()
        sol2 = follow3d(moves, grid)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
