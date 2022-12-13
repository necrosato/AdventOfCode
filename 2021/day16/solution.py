import time
import sys

def parsePacket(binstr, versionSet):
    version = int(binstr[0:3], 2)
    versionSet.add(version)
    tid = int(binstr[3:6], 2)
    rest = binstr[6:]
    print()
    print('Version: {} Type Id: {} bin: {}'.format(version, tid, binstr))
    if tid == 4:
        groups = [rest[i:i+5] for i in range(0, len(rest), 5)]
        bn = ''.join([group[1:] for group in groups])
        n = int(bn, 2)
        print(n)
    else:
        ltid = int(rest[0])
        rest = rest[1:]
        print('Length type id: {}'.format(ltid))
        subpackets = []
        if ltid == 0:
            nextPacketsLength = int(rest[0:15], 2)
            print('next packets length {}'.format(nextPacketsLength))
            rest = rest[15:]
            spbin = rest[0:nextPacketsLength]
            print(spbin)
        else:
            nextPacketCount = int(rest[0:11], 2)
            print('next packet count {}'.format(nextPacketCount))
            rest = rest[11:]
            subpacketlen = len(rest)//nextPacketCount
            subpackets = [rest[i:i+subpacketlen] for i in range(0, len(rest), subpacketlen)]
        print(subpackets)
        for packet in subpackets:
            parsePacket(packet, versionSet)
    print('Version {} done parsing\n'.format(version))


for fname in sys.argv[1:]:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        binstr = ''
        print(lines[0])
        for c in lines[0]:
            if ord(c) > 57:
                b = ord(c)-55
            else:
                b = int(c)
            binstr += format(b, '#06b')[2:]
        binstr = binstr[0:-7] + binstr[-7:].rstrip('0')
        versionSet = set()
        parsePacket(binstr, versionSet)
        end = time.time()
        solution = sum(versionSet)
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
