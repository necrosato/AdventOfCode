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

def make_hand_dict(hand):
    hand_dict = {}
    for c in hand:
        if c not in hand_dict:
            hand_dict[c] = 0
        hand_dict[c] += 1
    return hand_dict

def n_kind(hand_dict, n):
    return max(hand_dict.values()) == n

def five_kind(hand_dict):
    return n_kind(hand_dict, 5)

def four_kind(hand_dict):
    return n_kind(hand_dict, 4)

def three_kind(hand_dict):
    return n_kind(hand_dict, 3)

def full_house(hand_dict):
    return sorted(hand_dict.values()) == [2, 3]

def two_pair(hand_dict):
    return sorted(hand_dict.values()) == [1, 2, 2]

def one_pair(hand_dict):
    return sorted(hand_dict.values()) == [1, 1, 1, 2]

def high_card(hand_dict):
    return set(hand_dict.values()) == {1}

hand_types = [five_kind, four_kind, full_house, three_kind, two_pair, one_pair, high_card]

def sort_buckets(buckets, order):
    card_ranks = { order[i]:i for i in range(len(order)) }
    for b in buckets:
        b[1] = sorted(b[1], key=lambda x: tuple(card_ranks[c] for c in x[0]))
    return reversed(buckets)
 
def sum_ranks(buckets):
    rank = 1
    total = 0
    for b in buckets:
        for hand in b[1]:
            total += rank*hand[1]
            rank += 1
    return total

@timer_func
def part1( hands ):
    buckets = [ [t, []] for t in hand_types ]
    for hand, bet in hands:
        hand_dict = make_hand_dict(hand)
        for hand_type, bucket in buckets:
            if hand_type(hand_dict):
                bucket.append((hand, bet))
                break
    return sum_ranks(sort_buckets(buckets, '23456789TJQKA'))

@timer_func
def part2( hands ):
    buckets = [ [t, []] for t in hand_types ]
    for hand, bet in hands:
        for hand_type, bucket in buckets:
            hand_dict = make_hand_dict(hand)
            if 'J' in hand_dict:
                found = False
                js = hand_dict.pop('J')
                if js == 5 and hand_type == five_kind:
                    bucket.append((hand, bet))
                    found = True
                    break
                for c in hand_dict:
                    hand_dict[c] += js
                    if hand_type(hand_dict):
                        bucket.append((hand, bet))
                        found = True
                        break
                    hand_dict[c] -= js
                if found:
                    break
            else:
                if hand_type(hand_dict):
                    bucket.append((hand, bet))
                    break
    return sum_ranks(sort_buckets(buckets, 'J23456789TQKA'))

def main():
    args = parseArgs()
    for input_file_name in args.input:
        with open(input_file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            hands = [(l.split()[0], int(l.split()[1])) for l in lines]
            sol1 = part1(hands)
            sol2 = part2(hands)
        
if __name__=='__main__':
    main()
