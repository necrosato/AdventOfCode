import time

class Item:
    def __init__(self, val):
        self.val = val

class Monkey:
    def __init__(self, n, items, operation, test, if_true, if_false):
        self.n = n
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.throws = 0
        self.maxWorry = 0
    
    def throw(self, item, to, monkeys):
        monkeys[to].items.append(item)

    def turn(self, monkeys):
        for i in range(len(self.items)):
            o = self.operate(self.items[i])
            if self.testItem(o):
                self.throw(o, self.if_true, monkeys)
            else:
                self.throw(o, self.if_false, monkeys)
            self.throws += 1
        self.items = []

    def testItem(self, item):
        item.val = item.val % self.maxWorry
        return item.val % self.test == 0

    def operate(self, item):
        f = item.val if self.operation[1] == 'old' else int(self.operation[1])
        operation = (self.operation[0], f)
        if self.operation[0] == '+':
            item.val += f
        if self.operation[0] == '*':
            item.val *= f
# set to true for part 1, false for part2
        if False:
            item.val //= 3
        return item

for fname in ['input.txt', 'input2.txt']:
    solution = 0
    with open(fname, 'r') as f:
        monkeys = []
        maxWorry = 1
        for chunk in f.read().split('\n\n'):
            chunk = chunk.split('\n')
            n = int(chunk[0].split()[1][0])
            items = [Item(int(i)) for i in chunk[1].split(':')[1].strip().split(', ')]
            operation = tuple(chunk[2].split()[-2:])
            test = int(chunk[3].split()[-1])
            maxWorry *= test
            if_true = int(chunk[4].split()[-1])
            if_false = int(chunk[5].split()[-1])
            monkeys.append(Monkey(n, items, operation, test, if_true, if_false))
        for monkey in monkeys:
            monkey.maxWorry = maxWorry

        start = time.time()
        rounds = 10000
        for i in range(rounds):
            for monkey in monkeys:
                monkey.turn(monkeys)
        solution = list(sorted(monkeys, key=lambda x: x.throws))[-2:]
        solution = solution[0].throws * solution[1].throws
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, solution, end-start))
