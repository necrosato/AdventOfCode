import time

def move(coords, direction, count):
    if direction == 'D':
        return (coords[0], coords[1]+count)
    if direction == 'U':
        return (coords[0], coords[1]-count)
    if direction == 'L':
        return (coords[0]-count, coords[1])
    if direction == 'R':
        return (coords[0]+count, coords[1])
def follow(head, tail):
    newx = tail[0]
    newy = tail[1]
    xdiff = abs(head[0] - tail[0])
    ydiff = abs(head[1] - tail[1])
    if xdiff > 1:
        newx = tail[0] + ( xdiff-1 if head[0] > tail[0] else -1*xdiff+1 )
        if ydiff > 0:
            newy = tail[1] + ( 1 if head[1] > tail[1] else -1 )
    elif ydiff > 1:
        newy = tail[1] + ( ydiff-1 if head[1] > tail[1] else -1*ydiff+1 )
        if xdiff > 0:
            newx = tail[0] + ( 1 if head[0] > tail[0] else -1 )
    return (newx, newy)

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        tails = set()
        rope = []
        for i in range(10):
            rope.append((0, 0))
        tails.add(rope[-1])
        for line in lines:
            direction, count = line.split()
            count = int(count)
            for i in range(count):
                rope[0] = move(rope[0], direction, 1)
                for j in range(1, len(rope)):
                    rope[j] = follow(rope[j-1], rope[j])
                tails.add(rope[-1])
        solution = len(tails)
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
