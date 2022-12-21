import time
import sys

def part1( grid ):
    pass
def part2( grid ):
    pass

class Blueprint:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
        self.ore_bot_cost = int(instructions[0].split()[4])
        self.cla_bot_cost = int(instructions[1].split()[4])
        self.obs_bot_cost = (int(instructions[2].split()[4]), int(instructions[2].split()[7]))
        self.geo_bot_cost = (int(instructions[3].split()[4]), int(instructions[3].split()[7]))
    def __repr__(self):
        return self.name + str(self.instructions)

class Simulation:
    def __init__(self, blueprint, minutes=24):
        self.ore = 0
        self.cla = 0
        self.obs = 0
        self.geo = 0
        self.ore_bots = 1
        self.cla_bots = 0
        self.obs_bots = 0
        self.geo_bots = 0
        self.minutes = minutes
        self.blueprint = blueprint

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        blueprints = {}
        simulations = {}
        for line in lines:
            name, instructions = line.split(': ')
            instructions = instructions.split('. ')
            blueprints[name] = Blueprint(name, instructions)
            simulations[name] = Simulation(blueprints[name])
        print(simulations)
        grid = []
        p1 = time.time()
        sol1 = part1(grid)
        p2 = time.time()
        sol2 = part2(grid)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
