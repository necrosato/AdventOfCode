import time
endToPoints = {
    '}': 1197,
    ']': 57,
    ')': 3,
    '>': 25137
}
endToPoints2 = {
    '{': 3,
    '[': 2,
    '(': 1,
    '<': 4 
}
startToEnd = {
    '{': '}',
    '[': ']',
    '(': ')',
    '<': '>'
}
starts = '{[(<'
for fname in ['input2.txt']:
    solution = 0
    solution2 = []
    with open(fname, 'r') as f:
        start = time.time()
        for line in [l.strip() for l in f.readlines()]:
            linesolution = 0
            linesolution2 = 0
            stack = []
            for char in line:
                if char in starts:
                    stack.append(char)
                else:
                    last = stack.pop()
                    if startToEnd[last] != char:
                        linesolution += endToPoints[char]
                        print('expected {} but found {} instead'.format(startToEnd[last], char))
            if linesolution == 0:
                for char in reversed(stack):
                    linesolution2 *= 5
                    linesolution2 += endToPoints2[char]
                solution2.append(linesolution2)
            solution += linesolution
        solution2 = sorted(solution2)[len(solution2)//2]
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
