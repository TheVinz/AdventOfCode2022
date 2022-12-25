import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 54

class MyMap:
    def __init__(self, data):
        self.blizzards = []
        self.data = data
        self.sizex = len(data)-2
        self.sizey = len(data[0])-2

        for i in range(1, len(data)-1):
            for j in range(1, len(data[i])-1):
                c = data[i][j]
                if c in '><v^':
                    self.append(Blizzard((i-1,j-1), c))
        
        self.freeSpots = self.computeFreeSpots()
    
    def computeFreeSpots(self):
        end = self.draw()
        res = []

        x = []
        for i in range(len(end)):
            for j in range(len(end[i])):
                if end[i][j] == '.':
                    x.append((i,j))
        res.append(x)
        
        self.step()
        tmp = self.draw()

        while tmp != end:
            x = []
            for i in range(len(tmp)):
                for j in range(len(tmp[i])):
                    if tmp[i][j] == '.':
                        x.append((i,j))
            self.step()
            tmp = self.draw()
            res.append(x)
        
        return res

    def draw(self):
        res = []
        res.append('#.' + '#'*self.sizey)
        for _ in range(self.sizex):
            res.append('#'+'.'*self.sizey+'#')
        res.append('#'*self.sizey + '.#')

        for b in self.blizzards:
            x,y = b.position
            c = res[x+1][y+1]
            if c in '<>v^':
                c = '2'
            elif re.match(r'\d+', c):
                c = str(int(c)+1)
            elif c=='.':
                c = b.direction

            res[x+1] = res[x+1][:y+1] + c + res[x+1][y+2:]
        
        return res

    
    def append(self, blizzard):
        self.blizzards.append(blizzard)

    def step(self):
        for b in self.blizzards:
            b.update(self.sizex, self.sizey)

    def print(self):
        x = self.draw()

        for line in x:
            print(line)

class Blizzard:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
    
    def next(self, sizex, sizey):
        x, y = self.position
        match self.direction:
            case '^':
                return (x-1)%sizex, y
            case '>':
                return x, (y+1)%sizey
            case 'v':
                return (x+1)%sizex, y
            case '<':
                return x, (y-1)%sizey
            case _:
                raise Exception("Invalid direction {}".format(self.direction))
    
    def update(self, sizex, sizey):
        self.position = self.next(sizex, sizey)
    

def readInput(f):
    data = f.read().split('\n')

    return MyMap(data)

def shortestPath(model: MyMap, start, end, step=0):
    curr = set()
    curr.add(start)
    visited = [set() for _ in range(len(model.freeSpots))]
    visited[0].add(start)

    while len(curr)>0:
        step += 1
        idx = step%len(model.freeSpots)
        freeSpots = model.freeSpots[idx]
        next = set()
        for c in curr:
            if c==end:
                return step-1
            
            visited[idx].add(c)

            x,y = c
            for (i,j) in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]:
                    nx, ny = x+i, y+j
                    if (nx,ny) in freeSpots and (nx,ny) not in visited[(step+1)%len(model.freeSpots)]:
                        next.add((nx,ny))
        curr = next
        next = []
    
    raise Exception('Feasible path from {} to {} not found'.format(start, end))

def solve(model: MyMap):
    a = 0,1
    b = model.sizex+1, model.sizey

    res = shortestPath(model, a, b)
    res = shortestPath(model, b, a, res)
    return shortestPath(model, a, b, res)

if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        model = readInput(f)
    res = solve(model)

    if res == DEBUG:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(DEBUG, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        model = readInput(f)
    print(solve(model))