import time

class Cell:
    def __init__(self, val):
        self.val = val
        self.flashed = False

def getNeighbors(row, col):
    neighbors = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not ( i == 0 and j == 0 ):
                if row+i < 10 and row+i >= 0 and col+j < 10 and col+j >= 0:
                    neighbors.append((row+i, col+j))
    return neighbors

def updateCell(grid, row, col):
    grid[row][col].val += 1
    flashes = 0
    if not grid[row][col].flashed:
        if grid[row][col].val > 9:
            flashes = 1
            grid[row][col].flashed = True
            neighbors = getNeighbors(row, col)
            for neighbor in neighbors:
                flashes += updateCell(grid, neighbor[0], neighbor[1])
    return flashes

def live(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].flashed = False
            if grid[i][j].val > 9:
                grid[i][j].val = 0
    flashes = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            flashes += updateCell(grid, i, j)
    return flashes

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        grid = []
        for line in lines:
            row = []
            for char in line:
                row.append(Cell(int(char)))
            grid.append(row)
        steps = 100
        for i in range(steps):
            flashes=live(grid)
            solution+=flashes
        while flashes < 100:
            flashes = live(grid)
            steps += 1
        solution2 = steps

        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
