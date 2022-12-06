import time
def splitup(line, delims):
    if len(delims) == 0:
        return line
    return [splitup(l, delims[1:]) for l in line.split(delims[0])]


def expand(start, end, diags=False):
    expanded = []
    xdir = 1 if start[0] <= end[0] else -1
    ydir = 1 if start[1] <= end[1] else -1
    if start[1] == end[1] or start[0] == end[0]:
        for x in range(start[0], end[0]+xdir, xdir):
            for y in range(start[1], end[1]+ydir, ydir):
                expanded.append((x, y))
    elif diags and abs(end[0]-start[0]) == abs(end[1]-start[1]):
        for i in range(abs(end[0]-start[0])+1):
            expanded.append((start[0]+(i*xdir), start[1]+(i*ydir)))
    return expanded


def count(line, output):
    parts = splitup(line, [' -> ', ','])
    parts = [ [ int(p) for p in part ] for part in parts ]
    coords = expand(parts[0], parts[1])
    for coord in coords:
        if coord not in output:
            output[coord] = 0
        output[coord] += 1

def count2(line, output):
    parts = splitup(line, [' -> ', ','])
    parts = [ [ int(p) for p in part ] for part in parts ]
    coords = expand(parts[0], parts[1], True)
    for coord in coords:
        if coord not in output:
            output[coord] = 0
        output[coord] += 1


for fname in ['input.txt', 'input2.txt']:
    counters = {}
    counters2 = {}
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        start = time.time()
        for line in [l.strip() for l in f.readlines()]:
            count(line, counters)
            count2(line, counters2)
        for coord in counters:
            if counters[coord] > 1:
                solution+=1
        for coord in counters2:
            if counters2[coord] > 1:
                solution2+=1
        end = time.time()
    print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
