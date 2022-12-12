import time

class Monkey:
    def __init__(self, n, items, operation, test, if_true, if_false):
        self.n = n
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.throws = 0
    
    def throw(self, i, to, monkeys):
        #print('monkey {} throwing {} to monkey {}'.format(self.n, i, to))
        monkeys[to].items.append(i)

    def turn(self, monkeys):
        for i in range(len(self.items)):
            o = self.operate(self.items[i]) // 3
            if o % self.test == 0:
                self.throw(o, self.if_true, monkeys)
            else:
                self.throw(o, self.if_false, monkeys)
            self.throws += 1
        self.items = []

    def operate(self, n):
        f = n if self.operation[1] == 'old' else int(self.operation[1])
        if self.operation[0] == '+':
            return n + f
        if self.operation[0] == '*':
            return n * f


for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    with open(fname, 'r') as f:
        monkeys = []
        for chunk in f.read().split('\n\n'):
            chunk = chunk.split('\n')
            n = chunk[0].split()[1][0]
            items = [int(i) for i in chunk[1].split(':')[1].strip().split(', ')]
            operation = chunk[2].split()[-2:]
            test = int(chunk[3].split()[-1])
            if_true = int(chunk[4].split()[-1])
            if_false = int(chunk[5].split()[-1])
            #print((items, operation, test, if_true, if_false))
            monkeys.append(Monkey(n, items, operation, test, if_true, if_false))
        start = time.time()
        rounds = 300
        for i in range(rounds):
            for monkey in monkeys:
                monkey.turn(monkeys)

        #print([m.throws for m in monkeys])
        solution = list(sorted(monkeys, key=lambda x: x.throws))[-2:]
        solution = solution[0].throws * solution[1].throws
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
