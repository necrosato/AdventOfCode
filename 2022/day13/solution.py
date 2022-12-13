import time
import functools

def parsePacket(packetstr):
    packetstr = packetstr.strip(',')
    if packetstr == '[]':
        return ([], 1)
    packet = []
    partstart = 0
    i = 1
    while i < len(packetstr):
        if packetstr[i] == '[':
            sub = packetstr[partstart:i].strip('[').strip(',').strip(']')
            new = packetstr[i:]
            if len(sub) > 0:
                packet += [int(s) for s in sub.strip(',').split(',')]
            subpacket, subend = parsePacket(new)
            packet.append(subpacket)
            partstart = i+subend+1
            i = partstart
        elif packetstr[i] == ']':
            sub = packetstr[partstart:i+1].strip('[').strip(',').strip(']')
            if len(sub) > 0:
                packet += [int(s) for s in sub.split(',')]
            return (packet, i)
        else:
            i += 1
    return (packet, i)
    
def compare(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return -1
        if left > right:
            return 1
        if left == right:
            return 0
    if type(left) == list and type(right) == list:
        for i in range(max(len(left), len(right))):
            if i >= len(left):
                return -1
            if i >= len(right):
                return 1
            c = compare(left[i],right[i])
            if c != 0:
                return c
    if type(left) == int and type(right) == list:
        return compare([left], right)
    if type(left) == list and type(right) == int:
        return compare(left, [right])
    return 0

def check(lines):
    for i in range(0, len(lines), 2):
        c = compare(lines[i], lines[i+1])
        if c != -1:
            return c
    return -1

for fname in ['input2.txt', 'input.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        start = time.time()
        pairs = [pair.split('\n') for pair in f.read().split('\n\n')]
        for i in range(len(pairs)):
            left = parsePacket(pairs[i][0])[0]
            right = parsePacket(pairs[i][1])[0]
            if compare(left, right) == -1:
                solution += i+1
        lines = []
        dividers = [[[2]], [[6]]]
        for pair in pairs:
            lines.append(parsePacket(pair[0])[0])
            lines.append(parsePacket(pair[1])[0])
        lines = sorted(lines+dividers, key=functools.cmp_to_key(compare))
        if check(lines) == -1:
            print('sorted passed')
            solution2 = (lines.index(dividers[0])+1)*(lines.index(dividers[1])+1)
            end = time.time()
            print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
