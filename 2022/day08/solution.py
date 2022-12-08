import time

class Tree:
    def __init__(self, height, visible=False):
        self.height = height
        self.visible = visible
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

def edgeParts(grid, row, col):
    parts = []
    parts.append(reversed(grid[row][0:col]))
    parts.append(grid[row][col+1:])
    parts.append(reversed([grid[i][col] for i in range(row)]))
    parts.append([grid[i][col] for i in range(row+1, len(grid))])
    return parts

def checkTree(grid, row, col):
    if grid[row][col].visible:
        return True
    if row == 0 or row == len(grid)-1 or col == 0 or col == len(grid)-1:
        grid[row][col].visible = True
        return True
    for part in edgeParts(grid, row, col):
        if max(part) < grid[row][col]:
            grid[row][col].visible = True
            break

def scoreTree(grid, row, col):
    if row == 0 or row == len(grid)-1 or col == 0 or col == len(grid)-1:
        return 0
    score = 1
    for part in edgeParts(grid, row, col):
        factor = 0
        for tree in part:
            factor += 1
            if tree >= grid[row][col]:
                break
        score *= factor
    return score 

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        grid = []
        scores = []
        start = time.time()

        for line in [l.strip() for l in f.readlines()]:
            row = []
            srow = []
            for tree in line:
                height = int(tree)
                row.append(Tree(height))
                srow.append(0)
            grid.append(row)
            scores.append(srow)

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                checkTree(grid, i, j)
                scores[i][j] = scoreTree(grid, i, j)

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].visible:
                    solution += 1
                solution2 = max(solution2, scores[i][j])
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
