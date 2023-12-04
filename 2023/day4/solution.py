import argparse
import time

def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s returned {result}')
        return result
    return wrap_func

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

@timer_func
def part1( tickets ):
    score = 0
    for t in tickets:
        wr = set(t[1]) - set(t[2])
        match = len(t[1]) - len(wr)
        if match > 0:
            score += pow(2, match-1)
    return score

@timer_func
def part2( tickets ):
    tickets = { int(t[0].split()[1]): t for t in tickets }
    won = { tn: 1 for tn in tickets }
    for tn in tickets:
        t = tickets[tn]
        wr = set(t[1]) - set(t[2])
        match = len(t[1]) - len(wr)
        if match > 0:
            for i in range(tn+1, tn+match+1):
                won[i] += won[tn]
    return sum([won[k] for k in won])

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            tickets = [ l.split(' | ') for l in lines ]
            tickets = [ [ t[0].split(': '), [ int(n) for n in t[1].split() ] ] for t in tickets ]
            tickets = [ [ t[0][0], [ int(n) for n in t[0][1].split() ], t[1] ] for t in tickets ]
            sol1 = part1(tickets)
            sol2 = part2(tickets)
        
if __name__=='__main__':
    main()

