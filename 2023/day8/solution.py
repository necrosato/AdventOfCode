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


def cycle(graph, seq, start):
    i = 0
    cur = start
    while cur[-1] != 'Z':
        d = seq[i%len(seq)]
        cur = graph[cur][d]
        i += 1
    return i

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

@timer_func
def part1( graph, seq ):
    return cycle(graph, seq, 'AAA', 'ZZZ')

@timer_func
def part2( graph, seq ):
    starts = {}
    for node in graph:
        if node[-1] == 'A':
            starts[node] = cycle(graph, seq, node)
    print(starts)
    total = 1
    factors = set()
    for start in starts:
        factors = factors.union(set(prime_factors(starts[start])))
    for factor in factors:
        total *= factor
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            seq = lines[0]
            graph = {}
            for line in lines[2:]:
                node, edges = line.split(' = ')
                l,r = edges[1:-1].split(', ')
                graph[node] = { 'L': l, 'R': r }
            sol1 = part1(graph, seq)
            sol2 = part2(graph, seq)
        
if __name__=='__main__':
    main()

