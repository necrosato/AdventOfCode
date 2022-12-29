import time
import sys
 
def part1( simulations ):
    qualities = []
    for simulation in simulations:
        s = time.time()
        vals, sim = simulations[simulation].run(24, set())
        qualities.append(vals[1][0] * sim.blueprint.id)
        print('simulation: {} vals: {} quality: {} took {} seconds'.format(simulation, vals, qualities[-1], time.time()-s))
    return sum(qualities)
        
def part2( simulations ):
    geodes = []
    for simulation in ['Blueprint 1', 'Blueprint 2', 'Blueprint 3']:
        if simulation in simulations:
            s = time.time()
            vals, sim = simulations[simulation].run(32, set())
            geodes.append(vals[1][0])
            print('simulation: {} vals: {} geodes: {} took {} seconds'.format(simulation, vals, geodes[-1], time.time()-s))
    prod = 1
    for gs in geodes:
        prod *= gs
    return prod

class Blueprint:
    def __init__(self, name, instructions):
        self.id = int(name.split()[1])
        self.ore_bot_cost = int(instructions[0].split()[4])
        self.cla_bot_cost = int(instructions[1].split()[4])
        self.obs_bot_cost = (int(instructions[2].split()[4]), int(instructions[2].split()[7]))
        self.geo_bot_cost = (int(instructions[3].split()[4]), int(instructions[3].split()[7]))

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

    def state(self):
        return (self.minutes, (self.geo, self.obs, self.cla, self.ore), (self.geo_bots, self.obs_bots, self.cla_bots, self.ore_bots))

    def optimalGeodes(self, minutes):
        return self.geo + sum([(self.geo_bots + i) for i in range(minutes)])

    def run(self, minutes, visited, currentMax=None):
        if self.state() in visited or minutes == 0:
            visited.add(self.state())
            return self.state(), self
        if currentMax is None:
            currentMax = (self.state(), self)
        if currentMax[0][1][0] >= self.optimalGeodes(minutes):
            return currentMax
        visited.add(self.state())
        options = []
        if self.ore >= self.blueprint.geo_bot_cost[0] and self.obs >= self.blueprint.geo_bot_cost[1]:
            if self.ore_bots >= self.blueprint.geo_bot_cost[0] and self.obs_bots >= self.blueprint.geo_bot_cost[1]:
                self.geo = self.optimalGeodes(minutes)
                return self.state(), self
            options.append(Simulation(other=self))
            options[-1].ore -= self.blueprint.geo_bot_cost[0]
            options[-1].obs -= self.blueprint.geo_bot_cost[1]
            options[-1].collect()
            options[-1].geo_bots += 1
        else:
            options.append(self)
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
        results = []
        for option in options:
            if len(results) > 0 and currentMax[0][1][0] < results[-1][0][1][0]:
                currentMax = results[-1]
            results.append(option.run(minutes-1, visited, currentMax))
        return max(results, key=lambda x:x[0])

    def collect(self):
        self.ore += self.ore_bots
        self.cla += self.cla_bots
        self.obs += self.obs_bots
        self.geo += self.geo_bots
        self.minutes += 1

for fname in ['input', 'input2'] if len(sys.argv) < 2 else sys.argv[1:]:
    with open(fname, 'r') as f:
        ts = time.time()
        lines = [l.strip() for l in f.readlines()]
        simulations = {}
        simulations2 = {}
        for line in lines:
            name, instructions = line.split(': ')
            blueprint = Blueprint(name, instructions.split('. '))
            simulations[name] = Simulation(blueprint)
            simulations2[name] = Simulation(blueprint)
        p1 = time.time()
        sol1 = part1(simulations)
        p2 = time.time()
        print('{} part1: {} took {} seconds'.format(fname, sol1, p2-p1))
        sol2 = part2(simulations2)
        te = time.time()
        print('{} part2: {} took {} seconds'.format(fname, sol2, te-p2))
        print('{} total time {} seconds'.format(fname, te-ts))
