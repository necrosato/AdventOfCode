import argparse
import time
from collections import deque
import heapq

'''
some generic helper functions
'''
def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s returned {result}')
        return result
    return wrap_func

def vector_add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))
'''
end generic helper functions
'''

def parseArgs():
    parser = argparse.ArgumentParser(description='Advent of Code Solution', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, action='append', required=True,
        help='an input file path, can passed multiple times to run multiple test files')
    return parser.parse_args()

class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def cubes(self):
        c = set()
        for x in range(self.end[0]-self.start[0]+1):
            for y in range(self.end[1]-self.start[1]+1):
                for z in range(self.end[2]-self.start[2]+1):
                    c.add(vector_add(self.start,(x,y,z)))
        return c
    def next_cubes(self):
        c = set()
        for x in range(self.end[0]-self.start[0]+1):
            for y in range(self.end[1]-self.start[1]+1):
                for z in range(self.end[2]-self.start[2]+1):
                    c.add(vector_add(self.start,(x,y,z-1)))
        return c
    def fall(self):
        self.start[-1]-=1
        self.end[-1]-=1

@timer_func
def part1and2( bricks ):
    bricks = sorted(bricks,key=lambda x:x.start[-1])
    settled = set()
    for x in range(400):
        for y in range(400):
            settled.add((x,y,0))
    for i in range(200):
        for brick in bricks:
            if settled & brick.next_cubes():
                settled |= brick.cubes()
            else:
                brick.fall()
    total = 0
    total_falling = 0
    for brick in bricks:
        falling = 0
        temp = settled - brick.cubes()
        for b2 in bricks:
            if not (temp & b2.next_cubes())-b2.cubes():
                temp -= b2.cubes()
                falling += 1
        total += falling == 0
        total_falling += falling
    return total, total_falling

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            bricks = []
            for line in lines:
                start,end = line.split('~')
                start = list(map(int,start.split(',')))
                end = list(map(int,end.split(',')))
                bricks.append(Brick(start, end))
            part1and2(bricks)
         
if __name__=='__main__':
    main()

