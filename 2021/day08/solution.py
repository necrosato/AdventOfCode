import time

rules = {
    2: 'cf',
    3: 'acf',
    4: 'bcdf',
    7: 'abcdefg'
}

segments = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
}
# count how many times each segment is used across all possible digits
def getSegmentCounts(digits):
    counts = {}
    for char in 'abcdefg':
        count = 0
        for digit in digits:
            if char in digit:
                count +=1 
        if count not in counts:
            counts[count] = []
        counts[count].append(char)
    return counts

referenceCounts = getSegmentCounts(segments)
print('Reference segment usage in all possible digits to segment {}'.format(referenceCounts))

def mapUniqueSegmentCounts(signals, mappings):
    counts = getSegmentCounts(signals)
    for count in counts:
        if len(counts[count]) == 1:
            mappings[counts[count][0]] = referenceCounts[count][0]
    return mappings

def sigLenMap(siglist):
    signals = {}
    for i in range(2, 8):
        signals[i] = []
    for signal in siglist:
        signals[len(signal)].append(signal)
    return signals

def mapA(signals, mappings, siglenmap):
    c = list(set(siglenmap[3][0]) - set(siglenmap[2][0]))[0]
    mappings[c] = 'a'

def mapCF(signals, mappings, siglenmap, segcounts):
    onedig = siglenmap[2][0]
    if onedig[0] == segcounts[9][0]:
        mappings[onedig[0]] = 'f'
        mappings[onedig[1]] = 'c'
    else:
        mappings[onedig[1]] = 'f'
        mappings[onedig[0]] = 'c'

def mapDG(signals, mappings, siglenmap, segcounts):
    bd = list(set(siglenmap[4][0]) - set(siglenmap[2][0]))
    for char in bd:
        if not mappings[char].isalpha():
            mappings[char] = 'd'
    for char in mappings:
        if not mappings[char].isalpha():
            mappings[char] = 'g'

def translate(digits, mappings):
    translated = []
    for digit in digits:
        td = ''
        for char in digit:
            td += mappings[char]         
        translated.append(td)
    return translated

def makeMappings(signals):
    mappings = {
        'a': '_',
        'b': '_',
        'c': '_',
        'd': '_',
        'e': '_',
        'f': '_',
        'g': '_'
    }
    slm = sigLenMap(signals)
    mapUniqueSegmentCounts(signals, mappings)
    mapA(signals, mappings, slm)
    segcounts = getSegmentCounts(signals)
    mapCF(signals, mappings, slm, segcounts)
    mapDG(signals, mappings, slm, segcounts)
    return mappings

def mappedOutput(output, mappings):
    return ''.join([mappings[c] for c in output])

for fname in ['input.txt', 'input2.txt', 'input3.txt']:
    ndisplays = 4
    displays = {}
    for i in range(ndisplays):
        displays[i] = {}

    with open(fname, 'r') as f:
        start = time.time()
        solution = 0
        solution2 = 0
        for parts in [l.strip().split('|') for l in f.readlines()]:
            signals = parts[0].strip().split()
            outputs = parts[1].strip().split()
            mappings = makeMappings(signals)

            
            outputNumStr = ''
            for output in outputs:
                if len(output) in rules:
                    solution += 1 
                mo = mappedOutput(output, mappings)
                outputNumStr += str(segments[''.join(sorted(mo))])
            solution2 += int(outputNumStr)
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
