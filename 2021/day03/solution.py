import time
for fname in ['input.txt', 'input2.txt']:
    gamma = []
    epsilon = []
    with open(fname, 'r') as f:
        start = time.time()
        lines = [l.strip() for l in f.readlines()]
        for i in range(len(lines[0])):
            bitlist = [l[i] for l in lines]        
            if bitlist.count('0') > bitlist.count('1'):
                gamma.append('0')
                epsilon.append('1')
            else:
                gamma.append('1')
                epsilon.append('0')
        gamma = int(''.join(gamma), base=2)
        epsilon = int(''.join(epsilon), base=2)
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, gamma*epsilon, end-start))

