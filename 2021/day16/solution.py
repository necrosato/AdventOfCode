import time
import sys

class Packet:
    def __init__(self):
        self.packets = []
        self.val = None
        self.typeId = None
    def operate(self):
        if self.typeId == 0:
            return sum([p.operate() for p in self.packets])
        elif self.typeId == 1:
            o = 1
            for i in [p.operate() for p in self.packets]:
                o *= i
            return o
        elif self.typeId == 2:
            return min([p.operate() for p in self.packets])
        elif self.typeId == 3:
            return max([p.operate() for p in self.packets])
        elif self.typeId == 4:
            return self.val
        elif self.typeId == 5:
            return 1 if self.packets[0].operate() > self.packets[1].operate() else 0
        elif self.typeId == 6:
            return 1 if self.packets[0].operate() < self.packets[1].operate() else 0
        elif self.typeId == 7:
            return 1 if self.packets[0].operate() == self.packets[1].operate() else 0

def parsePacket(binstr, versions):
    packet = Packet()
    version = int(binstr[0:3], 2)
    packet.typeId = int(binstr[3:6], 2)
    rest = binstr[6:]
    plen = 6
    if packet.typeId == 4:
        i = 0
        group = []
        while rest[i] != '0':
            i+=5
        data = rest[0:i+5]
        packet.val = int(''.join([group[1:] for group in [data[j:j+5] for j in range(0, len(data), 5)]]), 2)
        plen += len(data)
    else:
        lenTypeId = int(rest[0])
        rest = rest[1:]
        plen += 1
        if lenTypeId == 0:
            nextPacketsLength = int(rest[0:15], 2)
            plen += 15 + nextPacketsLength
            rest = rest[15:15+nextPacketsLength]
            i = 0
            while i <= len(rest) - 11:#min packet length is 11
                subpacket = parsePacket(rest[i:], versions)
                packet.packets.append(subpacket[0])
                i += subpacket[1]
        else:
            nextPacketsCount = int(rest[0:11], 2)
            rest = rest[11:]
            i = 0
            plen += 11
            for j in range(nextPacketsCount):
                subpacket = parsePacket(rest[i:], versions)
                packet.packets.append(subpacket[0])
                i += subpacket[1]
                plen += subpacket[1]
    versions.append(version)
    return (packet, plen)

for fname in sys.argv[1:]:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        binstr = ''
        for c in lines[0]:
            b = ord(c)-55 if ord(c) > 57 else int(c)
            binstr += format(b, '#06b')[2:]
        start = time.time()
        versions = [] 
        packet = parsePacket(binstr, versions)
        solution = sum(versions)
        solution2 = packet[0].operate()
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
