i = 1
mi = 1
cals = 0
mcals = 0
with open('input2.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if line != '':
            cals += int(line)
        else:
            if cals > mcals:
                mcals = cals
                mi = i
            i += 1
            cals = 0
    if cals > mcals:
        mcals = cals
        mi = i
print('elf number {} (1-indexed) carrying {} calories'.format(mi, mcals))
