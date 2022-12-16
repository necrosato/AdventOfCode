import time
import sys

def part1( grid ):
    pass
def part2( grid ):
    pass

class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate 
        self.tunnels = tunnels
        self.open = False
    def __repr__(self):
        return '{} {} {} {}'.format(self.name, self.rate, self.tunnels, self.open)

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    minutes = 30
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        valves = []
        valvemap = {}
        for parts in [line.split() for line in lines]:
            valves.append(Valve(parts[1], int(parts[4].split('=')[-1][:-1]), [part.strip(',') for part in parts[9:]]))
            valvemap[valves[-1].name] = valves[-1]

        grid = []
        p1 = time.time()
        sol1 = part1(grid)
        p2 = time.time()
        sol2 = part2(grid)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
