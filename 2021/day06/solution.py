import time

class Fish:
    def __init__(self, timer):
        self.timer = timer
    def spawn(self):
        self.timer = 6
        return Fish(8)
    def __repr__(self):
        return str(self.timer)


for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        start = time.time()
        fish = []
        for i in f.readlines()[0].strip().split(','):
            fish.append(Fish(int(i)))
        days = 80 
        spawnCycles = days // 7
        for i in range(days):
            newFish = []
            for f in fish:
                if f.timer == 0:
                    newFish.append(f.spawn())
                else:
                    f.timer -= 1
            for f in newFish:
                fish.append(f)
            #print('day {}: {} fish: state: {}'.format(i+1, len(fish), fish))
            #print('day {}: {} fish'.format(i+1, len(fish)))
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, len(fish), end-start))
