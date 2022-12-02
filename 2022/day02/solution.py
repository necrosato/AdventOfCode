shapes = { 'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3 }

# returns points for p2
def play( p1, p2 ):
    if shapes[p1] == shapes[p2]:
        print("Tie!")
        return shapes[p2] + 3
    if (shapes[p1]%3)+1 == shapes[p2]:
        print("P2 Wins!")
        return shapes[p2] + 6
    print("P1 Wins!")
    return shapes[p2]


score = 0
with open('input2.txt', 'r') as f:
    for line in [l.strip() for l in f.readlines()]:
        p1, p2 = line.split()
        print('{} vs {}'.format(shapes[p1], shapes[p2]))
        score += play(p1, p2)
        print(score)

print(score)
