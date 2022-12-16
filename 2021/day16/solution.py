import time
import sys

minPacketLength = 11 # number packets have at least one 5-bit chunk and a 6 bit header

class Packet:
    def __init__(self):
        self.packets = []
        self.val = None
        self.version = None
        self.typeId = None
        self.lenTypeId = None
        self.lenTypeBits = None
        self.nextPacketsLength = None
        self.nextPacketsCount = None 
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
    if len(binstr) < minPacketLength:
        return None
    packet.version = int(binstr[0:3], 2)
    packet.typeId = int(binstr[3:6], 2)
    rest = binstr[6:]
    plen = 6
    print('\nVersion: {} Type Id: {} bin: {}'.format(packet.version, packet.typeId, binstr))
    if packet.typeId == 4:
        i = 0
        group = []
        while rest[i] != '0':
            i+=5
        data = rest[0:i+5]
        bn = ''.join([group[1:] for group in [data[j:j+5] for j in range(0, len(data), 5)]])
        packet.val = int(bn, 2)
        plen += len(data)
    else:
        packet.lenTypeId = int(rest[0])
        rest = rest[1:]
        plen += 1
        print('Length type id: {}'.format(packet.lenTypeId))
        if packet.lenTypeId == 0:
            packet.nextPacketsLength = int(rest[0:15], 2)
            print('next packets length {}'.format(packet.nextPacketsLength))
            plen += 15 + packet.nextPacketsLength
            rest = rest[15:15+packet.nextPacketsLength]
            i = 0
            while i <= len(rest) - minPacketLength:
                subpacket = parsePacket(rest[i:], versions)
                if subpacket is not None:
                    packet.packets.append(subpacket[0])
                    i += subpacket[1]
                else:
                    print('found invalid packet: {}'.format(rest[i:]))
                    break
            data = rest[0:packet.nextPacketsLength]
        else:
            packet.nextPacketsCount = int(rest[0:11], 2)
            print('next packet count {}'.format(packet.nextPacketsCount))
            rest = rest[11:]
            i = 0
            plen += 11
            for j in range(packet.nextPacketsCount):
                subpacket = parsePacket(rest[i:], versions)
                if subpacket is not None:
                    packet.packets.append(subpacket[0])
                    i += subpacket[1]
                    plen += subpacket[1]
                else:
                    print('found invalid packet: {}'.format(rest[i:]))
                    break
    print('version {} done parsing length {}\n'.format(packet.version, plen))
    versions.append(packet.version)
    return (packet, plen)

for fname in sys.argv[1:]:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        binstr = ''
        print('Input: ' + lines[0])
        for c in lines[0]:
            if ord(c) > 57:
                b = ord(c)-55
            else:
                b = int(c)
            binstr += format(b, '#06b')[2:]
        versions = [] 
        packet = parsePacket(binstr, versions)
        solution = sum(versions)
        solution2 = packet[0].operate()
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
