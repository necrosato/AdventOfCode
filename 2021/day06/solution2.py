import time

class Fish:
    def __init__(self, timer):
        self.timer = timer
    def spawn(self):
        self.timer = 6
        return Fish(8)
    def __repr__(self):
        return str(self.timer)

    def willSpawn(self, days):
        return 1 + (days-self.timer-1) // 7

    def totalFamily(self, days):
        total = 2
        for i in range(self.willSpawn(days)-1):
            total *= 2
        return total


for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        start = time.time()
        fish = []
        for i in range(9):
            fish.append(0)
        for i in f.readlines()[0].strip().split(','):
            fish[int(i)] += 1
        print(fish)
        days = 256
        for i in range(days):
            new = fish[0] 
            fish = fish[1:] + [new]
            fish[6] += new
            #print(fish)
            #print(sum(fish))
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, sum(fish), end-start))
