import time
shapes = { 'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3 }
def play( p1, p2 ):
    if p1 == p2:
        return p2 + 3
    if (p1%3)+1 == p2:
        return p2 + 6
    return p2
def play2( p1, outcome ):
    if outcome == 'Y':
        return p1 + 3
    if outcome == 'Z':
        return (p1%3)+1 + 6
    return 3 if p1 == 1 else p1-1
score = 0
score2 = 0
with open('input2.txt', 'r') as f:
    start = time.time()
    for p1, p2 in [l.strip().split() for l in f.readlines()]:
        score += play(shapes[p1], shapes[p2])
        score2 += play2(shapes[p1], p2)
    end = time.time()
print('part 1: {} part 2: {} took {} seconds'.format(score, score2, end-start))
