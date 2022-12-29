import threading
import time
import sys
 
def part1( simulations ):
    qualities = []
    for simulation in simulations:
        print('starting ' + simulation)
        s = time.time()
        vals, sim = simulations[simulation].run(24, set())
        e = time.time()
        print('{} took {} seconds'.format(simulation, e-s))
        simulations[simulation] = sim
        quality = vals[1][0] * simulations[simulation].blueprint.id
        qualities.append(quality)
        print('simulation: {} vals: {} quality: {}'.format(simulation, vals, quality))
    return sum(qualities)
        
def part2( simulations ):
    geodes = []
    for simulation in ['Blueprint 1', 'Blueprint 2', 'Blueprint 3']:
        print('starting ' + simulation)
        s = time.time()
        vals, sim = simulations[simulation].run(32, set())
        e = time.time()
        print('{} took {} seconds'.format(simulation, e-s))
        simulations[simulation] = sim
        gs = vals[1][0]
        geodes.append(gs)
        print('simulation: {} vals: {} geodes: {}'.format(simulation, vals, gs))
    prod = 1
    for gs in geodes:
        prod *= gs
    return prod

class Blueprint:
    def __init__(self, name, instructions):
        self.name = name
        self.id = int(name.split()[1])
        self.instructions = instructions
        self.ore_bot_cost = int(instructions[0].split()[4])
        self.cla_bot_cost = int(instructions[1].split()[4])
        self.obs_bot_cost = (int(instructions[2].split()[4]), int(instructions[2].split()[7]))
        self.geo_bot_cost = (int(instructions[3].split()[4]), int(instructions[3].split()[7]))
    def __repr__(self):
        return self.name + str(self.instructions)

class Simulation:
    def __init__(self, blueprint=None, other=None):
        self.ore = 0 if other is None else other.ore
        self.cla = 0 if other is None else other.cla
        self.obs = 0 if other is None else other.obs
        self.geo = 0 if other is None else other.geo
        self.ore_bots = 1 if other is None else other.ore_bots
        self.cla_bots = 0 if other is None else other.cla_bots
        self.obs_bots = 0 if other is None else other.obs_bots
        self.geo_bots = 0 if other is None else other.geo_bots
        self.minutes = 0 if other is None else other.minutes
        self.blueprint = blueprint if other is None else other.blueprint

    def ores(self):
        return (self.geo, self.obs, self.cla, self.ore)
    def bots(self):
        return (self.geo_bots, self.obs_bots, self.cla_bots, self.ore_bots)
    def state(self):
        return (self.minutes, self.ores(), self.bots())
    def optimalGeodes(self, minutes):
        return self.geo + sum([(self.geo_bots + i) for i in range(minutes)])


    def run(self, minutes, visited):
        if self.state() in visited or minutes == 0:
            visited.add(self.state())
            return self.state(), self
        visited.add(self.state())
        options = [self]
        if self.ore >= self.blueprint.geo_bot_cost[0] and self.obs >= self.blueprint.geo_bot_cost[1]:
            options.append(Simulation(other=self))
            options[-1].ore -= self.blueprint.geo_bot_cost[0]
            options[-1].obs -= self.blueprint.geo_bot_cost[1]
            options[-1].collect()
            options[-1].geo_bots += 1
        if self.ore >= self.blueprint.obs_bot_cost[0] and self.cla >= self.blueprint.obs_bot_cost[1] and self.obs_bots < self.blueprint.geo_bot_cost[1]:
            options.append(Simulation(other=self))
            options[-1].ore -= self.blueprint.obs_bot_cost[0]
            options[-1].cla -= self.blueprint.obs_bot_cost[1]
            options[-1].collect()
            options[-1].obs_bots += 1
        if self.ore >= self.blueprint.cla_bot_cost and self.cla_bots < self.blueprint.obs_bot_cost[1]:
            options.append(Simulation(other=self))
            options[-1].ore -= self.blueprint.cla_bot_cost
            options[-1].collect()
            options[-1].cla_bots += 1
        if self.ore >= self.blueprint.ore_bot_cost and self.ore_bots < max([self.blueprint.geo_bot_cost[0], self.blueprint.obs_bot_cost[0], self.blueprint.cla_bot_cost, self.blueprint.ore_bot_cost]):
            options.append(Simulation(other=self))
            options[-1].ore -= self.blueprint.ore_bot_cost
            options[-1].collect()
            options[-1].ore_bots += 1
        self.collect()
        return max([option.run(minutes-1, visited) for option in options], key=lambda x:x[0])

    def collect(self):
        self.ore += self.ore_bots
        self.cla += self.cla_bots
        self.obs += self.obs_bots
        self.geo += self.geo_bots
        self.minutes += 1

    def __repr__(self):
        return 'Simulation id:{}\n\tminutes: {}\n\tore: {}\n\tclay: {}\n\tobsidian: {}\n\tgeodes: {}\n\tore bots: {}\n\tclay bots: {}\n\tobsidian bots: {}\n\tgeode bots: {}\n'.format(self.blueprint.id, self.minutes,self.ore,self.cla,self.obs,self.geo,self.ore_bots,self.cla_bots,self.obs_bots,self.geo_bots)

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
        p1 = time.time()
        #sol1 = part1(simulations)
        sol1 = 0
        p2 = time.time()
        sol2 = part2(simulations)
        te = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
