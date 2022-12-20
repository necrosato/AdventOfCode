import time
import sys

shapes = [
    ([(-1, 0), (0, 0), (1, 0), (2, 0)], 1),
    ([(0, 0), (-1, -1), (0, -1), (1, -1), (0, -2)], 3),
    ([(1, 0), (1, -1), (-1, -2), (0, -2), (1, -2)], 3),
    ([(-1, 0), (-1, -1), (-1, -2), (-1, -3)], 4),
    ([(-1, 0), (0, 0), (-1, -1), (0, -1)], 2),
]

def checkCoords(coords, stationary, width):
    for coord in coords:
        if coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord in stationary:
            return False
    return True

class Rock:
    def __init__(self, coords, origin):
        self.coords = [(coord[0]+origin[0], coord[1]+origin[1]) for coord in coords]
        self.top = origin[1]
    def fall(self, move, stationary, width):
        xmod = -1 if  move == '<' else 1
        new = [(coord[0]+xmod, coord[1]) for coord in self.coords]
        if checkCoords(new, stationary, width):
            self.coords = new
        new = [(coord[0], coord[1]-1) for coord in self.coords]
        if checkCoords(new, stationary, width):
            self.coords = new
            self.top-=1
        else:
            for coord in self.coords:
                stationary.add(coord)
            return False
        return True

def getHeight(moves, n):
    rocks = 0
    width = 7
    height = -1
    stationary = set()
    mi = 0
    lastcycleheight = 0
    lastcyclerocks = 0
    while rocks < n:
        spawnpoint = (width//2, height+shapes[rocks%len(shapes)][1]+3)
        rock = Rock(shapes[rocks%len(shapes)][0], spawnpoint)
        while rock.fall(moves[mi%len(moves)], stationary, width):
            mi+=1
            if mi%len(moves)==0:
                print('cycled through instructions, gained {} height, {} rocks'.format(height-lastcycleheight, rocks-lastcyclerocks))
                lastcycleheight=height
                lastcyclerocks = rocks
        mi+=1
        rocks+=1
        height = max(height, rock.top)
    return height + 1

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        moves = [l.strip() for l in f.readlines()][0]
        p1 = time.time()
        sol1 = getHeight(moves, 2022)
        p2 = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        # these values are for first input file only, use part1 to analyze the cycles
        rocks = 1000000000000
        crg = 1740
        chg = 2759
        cycles = rocks//crg - 2
        cycleheight = chg*cycles
        cyclerocks = crg*cycles
        remainder = getHeight(moves, rocks-cyclerocks)
        sol2 = cycleheight + remainder
        te = time.time()
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
