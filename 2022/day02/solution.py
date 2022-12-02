import time
shapes = { 'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3 }
# returns points for p2
def play( p1, p2 ):
    if p1 == p2:
        return p2 + 3
    if (p1%3)+1 == p2:
        return p2 + 6
    return p2

score = 0
with open('input2.txt', 'r') as f:
    start = time.time()
    for line in [l.strip() for l in f.readlines()]:
        p1, p2 = line.split()
        score += play(shapes[p1], shapes[p2])
    end = time.time()

print('{} took {} seconds'.format(score, end-start))
