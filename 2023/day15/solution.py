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

def hash(s):
    val = 0
    for c in s:
        val = ( (val + ord(c)) * 17 ) % 256
    return val

@timer_func
def part1( lines ):
    return sum([hash(l) for l in lines])

@timer_func
def part2( lines ):
    boxes = { i: [] for i in range(256) }
    labels_to_lengths = {}
    for line in lines:
        if line[-2] == '=':
            label = line[:-2]
            box = hash(label)
            length = int(line[-1])
            labels_to_lengths[label] = length
            if label not in boxes[box]:
                boxes[box].append(label)
        if line[-1] == '-':
            label = line[:-1]
            box = hash(label)
            if label in boxes[box]:
                boxes[box].pop(boxes[box].index(label))
                labels_to_lengths.pop(label)
    return sum([(i+1) * (j+1) * labels_to_lengths[boxes[i][j]] for i in boxes for j in range(len(boxes[i]))])

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = f.read().strip().split(',')
            sol1 = part1(lines)
            sol2 = part2(lines)
        
if __name__=='__main__':
    main()
