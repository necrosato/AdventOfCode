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

def check_fold(block, i):
    check_len = min(i, len(block)-i)
    return list(reversed(block[i-check_len:i])) == block[i:i+check_len]

def string_mismatch(s1, s2):
    return sum([ s1[i] != s2[i] for i in range(len(s1))])
         
def check_smudge(block, i):
    check_len = min(i, len(block)-i)
    l = list(reversed(block[i-check_len:i]))
    r = block[i:i+check_len]
    return sum([string_mismatch(l[i], r[i]) for i in range(check_len)]) == 1

def rotate(block):
    return [ ''.join([ block[r][c] for r in range(len(block)) ]) for c in range(len(block[0]))]

def part(blocks, check_f):
    total = 0
    for hb, vb in blocks:
        for i in range(1, len(hb)):
            if check_f(hb, i):
                total += i * 100
                break
        for i in range(1, len(vb)):
            if check_f(vb, i):
                total += i
                break
    return total

@timer_func
def part1( blocks ):
    return part(blocks, check_fold)

@timer_func
def part2( blocks ):
    return part(blocks, check_smudge)

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            blocks = []
            bi = 0
            for i in range(len(lines)):
                if lines[i] == '':
                    blocks.append((lines[bi:i], rotate(lines[bi:i])))
                    bi = i+1
            blocks.append((lines[bi:], rotate(lines[bi:])))
            sol1 = part1(blocks)
            sol2 = part2(blocks)
        
if __name__=='__main__':
    main()
