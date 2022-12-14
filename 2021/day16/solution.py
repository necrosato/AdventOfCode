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
        self.data = None

def parsePacket(binstr):
    packet = Packet()
    if len(binstr) < minPacketLength:
        return None
    packet.version = int(binstr[0:3], 2)
    packet.typeId = int(binstr[3:6], 2)
    rest = binstr[6:]
    print('\nVersion: {} Type Id: {} bin: {}'.format(packet.version, packet.typeId, binstr))
    if packet.typeId == 4:
        packet.data = rest
        groups = [rest[i:i+5] for i in range(0, len(rest), 5)]
        bn = ''.join([group[1:] for group in groups])
        packet.val = int(bn, 2)
        print(packet.val)
    else:
        packet.lenTypeId = int(rest[0])
        rest = rest[1:]
        print('Length type id: {}'.format(packet.lenTypeId))
        if packet.lenTypeId == 0:
            packet.nextPacketsLength = int(rest[0:15], 2)
            print('next packets length {}'.format(packet.nextPacketsLength))
            rest = rest[15:]
            packet.data = rest[0:packet.nextPacketsLength]
            print(packet.data)
        else:
            packet.nextPacketsCount = int(rest[0:11], 2)
            print('next packet count {}'.format(packet.nextPacketsCount))
            rest = rest[11:]
            subpacketlen = len(rest)//packet.nextPacketsCount # ? 
            packet.data = [rest[i:i+subpacketlen] for i in range(0, len(rest), subpacketlen)]
            for pdata in packet.data:
                subpacket = parsePacket(pdata)
                if subpacket is None:
                    return None
                packet.packets.append(subpacket)
    print('version {} done parsing\n'.format(packet.version))
    return packet


'''
packetlengths = {
    'header':6,
    'lt': 1,
    'pl': 15,
    'pc': 11,
    'nc': 5
}

def parsePacket(binstr, versionSet):
    packet = []
    if len(binstr) < minPacketLength:
        return None
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
'''


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
        binstr = binstr[0:-7] + binstr[-7:].rstrip('0')
        versionSet = set()
        parsePacket(binstr)
        end = time.time()
        solution = sum(versionSet)
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
