import time
import os

class Node:
    def __init__(self, name, size=0):
        self.name = name
        self.size_ = size
    def size(self):
        return self.size_
    def __repr__(self):
        return self.name + ' ' + str(self.size())
class Directory(Node):
    def __init__(self, name):
        super().__init__(name)
        self.nodes = []
    def size(self):
        return sum([n.size() for n in self.nodes])
    def __repr__(self):
        return self.name + ' ' + ' ' + str(self.size()) + ' ' + str(self.nodes)

def getCD(current, arg, dirs):
    path = os.path.abspath(arg)
    if arg[0] != '/':
        path = os.path.abspath(os.path.join(current, arg))
    if path not in dirs:
        dirs[path] = Directory(path)
    return dirs[path]

for fname in ['input.txt', 'input2.txt']:
    dirs = {}
    with open(fname, 'r') as f:
        start = time.time()
        cd = '/'
        for line in [ l.strip() for l in f.readlines() ]:
            parts = line.split()
            if parts[0] == '$':
                if parts[1] == 'cd':
                    cd = getCD(cd, parts[2], dirs).name
            else:
                if parts[0].isnumeric():
                    node = Node(parts[1], int(parts[0]))
                else:
                    node = getCD(cd, parts[1], dirs)
                dirs[cd].nodes.append(node)

        solution = 0 
        thresh = 100000
        deleteDir = dirs['/']
        deleteThresh = 30000000 - (70000000 - deleteDir.size())
        for d in dirs:
            if dirs[d].size() <= thresh:
                solution += dirs[d].size()
            if dirs[d].size() >= deleteThresh and dirs[d].size() < deleteDir.size():
                deleteDir = dirs[d]
        solution2 = deleteDir.size()  
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
