import time

def unique(chars):
    s = set()
    for c in chars:
        s.add(c)
    return len(s) == len(chars)

def getUniqueWindowStart(line, windowSize):
    for i in range(0, len(line)-windowSize):
        window = line[i:i+windowSize]
        if unique(window):
            print(window)
            return i+windowSize
            
for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        line = f.readlines()[0].strip()
        start = time.time()
        solution = getUniqueWindowStart(line, 4)
        solution2 = getUniqueWindowStart(line, 14)
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
