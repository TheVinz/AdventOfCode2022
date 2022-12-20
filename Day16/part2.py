import re
import math

debug = 1707

debug_filename = "debug.txt"
input_filename = "input.txt"

class Node:
    def __init__(self, rate, neighbours):
        self.rate=rate
        self.neighbours=neighbours

class Valve:
    def __init__(self, graph, label):
        self.neighbours = distances(graph, label)
        self.rate = graph[label].rate

        todel = []

        for kk in self.neighbours.keys():
            if graph[kk].rate==0 and kk!='AA':
                todel.append(kk)
        
        for n in todel:
            del self.neighbours[n]

def getMinDistance(graph, source, dest):
    res = math.inf
    stack = [(source, 0)]
    visited = []

    while len(stack) > 0:
        curr, dist = stack.pop()
        if curr == dest:
            if dist < res:
                res = dist
        else:
            visited.append(curr)
            node = graph[curr]
            for i in node.neighbours:
                if i not in visited:
                    stack = [(i, dist+1), *stack]
        
    if res == math.inf:
        raise Exception("Cannot find path from {} to {}".format(source, dest))
    return res


def distances(graph, source):
    res = {}
    for n in graph:
        res[n] = getMinDistance(graph, source, n)
    
    return res

def helper(graph, currents, visited, times):
    bst = 0

    time = max(times)
    idx = min([i for i in range(len(times)) if times[i]==time])
    current = currents[idx]

    if time <=0:
        return bst

    for n in graph[current].neighbours:
        dst = graph[current].neighbours[n]
        residualTime = time-dst-1
        if n not in visited and residualTime>0:
            newCurrents = currents.copy()
            newCurrents[idx] = n
            newTimes = times.copy()
            newTimes[idx] = residualTime
            pressure = helper(graph, newCurrents, [*visited, n], newTimes)
            pressure = residualTime*graph[n].rate + pressure
            if pressure > bst:
                bst = pressure
    
    return bst


def solve(graph):
    return helper(graph, ['AA', 'AA'], ['AA'], [26, 26])

def getInput(f):
    graph = {}
    for line in f:
        match = re.match(r'Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)', line.strip())
        label = match.group(1)
        flowRate = int(match.group(2))
        neighbours = re.findall(r'(\w+)(?:, |)', match.group(3))

        graph[label] = Node(flowRate, neighbours)

    valveGraph = {}
    
    for l in graph:
        if graph[l].rate > 0 or l=='AA':
            valveGraph[l] = Valve(graph, l)
        
    return valveGraph

if __name__=='__main__':
    graph = {}
    with open(debug_filename, 'r') as f:
        graph = getInput(f)

    res = solve(graph)

    if res == debug:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(debug, res))
        exit(-1)
        
    with open(input_filename, 'r') as f:
        graph = getInput(f)
    
    print(solve(graph))
