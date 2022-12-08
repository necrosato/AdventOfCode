import time

class Spot:
    def __init__(self, height, lowpoint=True):
        self.height = height
        self.lowpoint = lowpoint
    def __repr__(self):
        return str(self.height)
    def __eq__(self, other):
        return self.height == other.height
    def __lt__(self, other):
        return self.height < other.height
    def __le__(self, other):
        return self.height <= other.height
    def __gt__(self, other):
        return self.height > other.height
    def __ge__(self, other):
        return self.height >= other.height

def isLow(grid, row, col):
    neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for coords in neighbors:
        if coords[0] >= 0 and coords[0] < len(grid):
            if coords[1] >= 0 and coords[1] < len(grid[coords[0]]):
                if grid[coords[0]][coords[1]] <= grid[row][col]:
                    grid[row][col].lowpoint=False
                    return False
    return True

# add coords to basin set if height at coords > input height and < 9
def expandBasin(basin, grid, row, col, height):
    neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for coords in neighbors:
         if coords[0] >= 0 and coords[0] < len(grid):
            if coords[1] >= 0 and coords[1] < len(grid[coords[0]]):
                #print('CHECKING ({}, {}) {} against neighbor ({}, {}) {}'.format(row, col, grid[row][col], coords[0], coords[1], grid[coords[0]][coords[1]]))
                if grid[coords[0]][coords[1]].height > grid[row][col].height and grid[coords[0]][coords[1]].height < 9:
                    basin.add(coords)
                    expandBasin(basin, grid, coords[0], coords[1], grid[coords[0]][coords[1]].height)

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 1
    with open(fname, 'r') as f:
        grid = []
        basins = []
        start = time.time()

        for line in [l.strip() for l in f.readlines()]:
            row = []
            for spot in line:
                height = int(spot)
                row.append(Spot(height))
            grid.append(row)

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if isLow(grid, i, j):
                    solution += grid[i][j].height + 1
                    basin = set()
                    basin.add((i, j))
                    expandBasin(basin, grid, i, j, grid[i][j].height)
                    basins.append(basin)
                    #print('{} {} {}'.format(i, j, grid[i][j]))
        for basin in list(reversed(sorted(basins, key=lambda x: len(x))))[0:3]:
            print(len(basin))
            solution2 *= len(basin)
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
