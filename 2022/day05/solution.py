import time
import copy

for fname in ['input.txt', 'input2.txt']:
    board = {}
    instructions = []
    boardDone = False
    with open(fname, 'r') as f:
        start = time.time()
        for line in [l.rstrip() for l in f.readlines()]:
            if not boardDone:
                for i in range(1, (len(line)+1)//4+1):
                    if i not in board:
                        board[i] = []
                    if line[i*4-3].isalpha():
                        board[i].append(line[i*4-3])
            else:
                parts = line.split()
                instructions.append([int(parts[1]), int(parts[3]), int(parts[5])])

            if line == '':
                boardDone = True
        board2 = copy.deepcopy(board)
        for instruction in instructions:
            board[instruction[2]] = list(reversed(board[instruction[1]][0:instruction[0]])) + board[instruction[2]]
            board2[instruction[2]] = board2[instruction[1]][0:instruction[0]] + board2[instruction[2]]
            board[instruction[1]] = board[instruction[1]][instruction[0]:]
            board2[instruction[1]] = board2[instruction[1]][instruction[0]:]
        solution = ''.join([board[i][0] for i in board])
        solution2 = ''.join([board2[i][0] for i in board2])
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
