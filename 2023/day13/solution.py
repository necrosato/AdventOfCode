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

def string_mismatch(s1, s2):
    return sum([ s1[i] != s2[i] for i in range(len(s1))])
         
def check_fold(block, i, tolerance):
    check_len = min(i, len(block)-i)
    l = list(reversed(block[i-check_len:i]))
    r = block[i:i+check_len]
    return sum([string_mismatch(l[i], r[i]) for i in range(check_len)]) == tolerance

def rotate(block):
    return [ ''.join([ block[r][c] for r in range(len(block)) ]) for c in range(len(block[0]))]

@timer_func
def part(blocks, tolerance):
    total = 0
    for pairs in blocks:
        for pair in pairs:
            for i in range(1, len(pair[0])):
                if check_fold(pair[0], i, tolerance):
                    total += i * pair[1]
    return total

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            blocks = f.read().strip().split('\n\n')
            blocks = [((block.split(), 100), (rotate(block.split()), 1)) for block in blocks]
            sol1 = part(blocks, 0)
            sol2 = part(blocks, 1)
        
if __name__=='__main__':
    main()
