import time

def foldCoords(coords, fold):
    for pair in coords:
        if fold[0] == 'x':
            if pair[0] > fold[1]:
                pair[0] -= 2 * (pair[0] - fold[1])
        elif fold[0] == 'y':
            if pair[1] > fold[1]:
                pair[1] -= 2 * (pair[1] - fold[1])


for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        coords = []
        folds = []
         
        parsing = True
        for line in lines:
            if line == '':
                parsing = False
            elif parsing:
                coords.append([int(p) for p in line.split(',')])
            else:
                parts = line.split()
                folds.append(parts[-1].split('='))
                folds[-1][-1] = int(folds[-1][-1])

        for fold in folds:
            foldCoords(coords, fold)
            if solution == 0:
                cset = set()
                for coord in coords:
                    cset.add(tuple(coord))
                solution = len(cset)
        mx = max([coord[0] for coord in coords]) +1
        my = max([coord[1] for coord in coords]) +1

        grid = [ [' ']*my for i in range(mx)]
        for g in grid:
            print(g)
        for coord in coords:
            grid[coord[0]][coord[1]] = '#'
        for g in grid:
            print(''.join(g))
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
