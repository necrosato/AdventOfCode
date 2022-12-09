import time
import copy
import os


class Node:
    def __init__(self, name):
        self.name = name
        self.nodes = []
    def __repr__(self):
        return str([n.name for n in self.nodes])
        #return self.name

def getPaths(graph, src, dst, visited):
    paths = set()
    for node in graph[src].nodes:
        if node.name == dst:
            paths.add(os.path.join(src, dst))
        else:
            v = copy.deepcopy(visited)
            if node.name not in visited or node.name.isupper():
                v.add(node.name)
                for path in getPaths(graph, node.name, dst, v):
                    paths.add(os.path.join(src, path))
    return paths

def getPaths2(graph, src, dst, visited, dupe):
    paths = set()
    #print('pathing {} to {}'.format(src, dst))
    for node in graph[src].nodes:
        #print('checking {} to {}'.format(src, node.name))
        if node.name == dst:
            paths.add(os.path.join(src, dst))
        else:
            v = copy.deepcopy(visited)
            if node.name not in visited or node.name.isupper():
                v.add(node.name)
                for path in getPaths2(graph, node.name, dst, v, dupe):
                    paths.add(os.path.join(src, path))
            elif node.name != 'start' and dupe == '':
                v.add(node.name)
                for path in getPaths2(graph, node.name, dst, v, node.name):
                    paths.add(os.path.join(src, path))

    return paths


for fname in ['input.txt', 'input2.txt']:
    solution = 0
    solution2 = 0
    graph = {}
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        start = time.time()
        for line in lines:
            n1, n2 = line.split('-')
            if n1 not in graph:
                graph[n1] = Node(n1)
            if n2 not in graph:
                graph[n2] = Node(n2)
            graph[n1].nodes.append(graph[n2])
            graph[n2].nodes.append(graph[n1])
        visited = set()
        visited.add('start')
        paths = getPaths(graph, 'start', 'end', visited)
        paths2 = getPaths2(graph, 'start', 'end', visited, '')
        solution = len(paths)
        solution2 = len(paths2)
        end = time.time()
        print('{} solution: {} solution2: {} took {} seconds'.format(fname, solution, solution2, end-start))
