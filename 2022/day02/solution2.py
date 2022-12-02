import time
shapes = { 'A': 1, 'B': 2, 'C': 3}
# returns points for p2
def play( p1, outcome ):
    if outcome == 'Y':
        return shapes[p1] + 3
    if outcome == 'Z':
        return (shapes[p1]%3)+1 + 6
    return 3 if p1 == 'A' else shapes[p1]-1

score = 0
with open('input2.txt', 'r') as f:
    start = time.time()
    for line in [l.strip() for l in f.readlines()]:
        p1, p2 = line.split()
        score += play(p1, p2)
    end = time.time()

print('{} took {} seconds'.format(score, end-start))
