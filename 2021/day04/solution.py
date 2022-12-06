import time
def check(card):
    for line in card:
        if line.count('X') == 5:
            return True
    for i in range(len(card[0])):
        if [line[i] for line in card].count('X') == 5:
            return True
    return False

def unmarkedSum(card):
    ret = 0
    for line in card:
        for n in line:
            if n != 'X':
                ret += int(n)
    return ret


for fname in ['input.txt', 'input2.txt']:
    done = False
    with open(fname, 'r') as f:
        start = time.time()
        lines = [l.strip() for l in f.readlines()]
        draws = lines[0].split(',')
        cards = []
        card = []
        for line in lines[2:]:
            if line == '':
                cards.append(card)
                card = []
            else:
                card.append(line.split())
        cards.append(card)

        for n in draws:
            for card in cards:
                if not done:
                    for line in card:
                        for i in range(len(line)):
                            if line[i] == n:
                                line[i] = 'X'
                    if check(card):
                        print(card)
                        solution = unmarkedSum(card) * int(n)
                        end = time.time()
                        print('{} solution: {} took {} seconds'.format(fname, solution, end-start))
                        done = True

