shapes = { 'A': 1, 'B': 2, 'C': 3}

# returns points for p2
def play( p1, outcome ):
    if outcome == 'Y':
        print("Tie!")
        return shapes[p1] + 3
    if outcome == 'Z':
        print("P2 Wins!")
        return (shapes[p1]%3)+1 + 6
    print("P1 Wins!")
    return 3 if p1 == 'A' else shapes[p1]-1


score = 0
with open('input2.txt', 'r') as f:
    for line in [l.strip() for l in f.readlines()]:
        p1, p2 = line.split()
        print('{} vs {}'.format(shapes[p1], p2))
        score += play(p1, p2)
        print(score)

print(score)
