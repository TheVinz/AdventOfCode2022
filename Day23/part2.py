debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 20

class Elf:
    def __init__(self, pos):
        self.pos = pos
        self.directions = '^v<>'
    
    def _getMatrix(self, elves):
        res = [[0 for _ in range(3)] for _ in range(3)]

        x,y = self.pos

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i,j) != (0,0):
                    if (x+i, y+j) in elves:
                        res[i+1][j+1] = 1
        
        return res

    def _canMove(self, direction, matrix):
        match direction:
            case '^':
                return sum(matrix[0])==0
            case '>':
                return sum([matrix[i][2] for i in range(3)]) == 0
            case 'v':
                return sum(matrix[2])==0
            case '<':
                return sum([matrix[i][0] for i in range(3)]) == 0
            case '.':
                return True
            case _:
                raise Exception("Invalid direction {}".format(direction))


    def getMove(self, positions):
        m = self._getMatrix(positions)

        if sum([sum(m[i]) for i in range(3)]) == 0:
            return '.'

        for d in self.directions:
            if self._canMove(d, m):
                return d
        
        return '.'

    def getDest(self, direction):
        x,y = self.pos
        match direction:
            case '^':
                return x-1, y
            case '>':
                return x, y+1
            case 'v':
                return x+1, y
            case '<':
                return x, y-1
            case '.':
                return x, y
            case _:
                raise Exception("Invalid direction {}".format(direction))
    
    def move(self, dir):
        pos = self.getDest(dir)
        self.pos=pos

        self.directions = self.directions[1:] + self.directions[0]

def printMap(elves, coords):
    maxx = -10e7
    minx = 10e7
    maxy = -10e7
    miny = 10e7

    for e in elves:
        x,y = e.pos
        if x>maxx:
            maxx = x
        if x<minx:
            minx=x
        if y>maxy:
            maxy=y
        if y<miny:
            miny=y
    
    print('+' + '-'*(maxy-miny+1) + '+')
    for x in range(minx, maxx+1):
        print('|', end='')
        for y in range(miny, maxy+1):
            if (x, y) in coords:
                print('#', end='')
            else:
                print('.', end='')
        print('|')
    print('+' + '-'*(maxy-miny+1) + '+')

def readInput(f):
    elves = []
    coords = {}

    data = f.read().split('\n')
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '#':
                e = Elf((i,j))
                elves.append(e)
                coords[(i,j)] = e
    
    model = elves, coords
    # printMap(*model)
    
    return model


def solve(model):
    elves, coords = model
    converged = False
    it = 0

    while not converged:
        it += 1
        converged = True
        conflicts = {}
        step = {}
        for e in elves:
            m = e.getMove(coords)
            dest = e.getDest(m)
            if dest not in conflicts.keys():
                conflicts[dest] = 0
            conflicts[dest]+=1
            step[e] = m
        
        coords = []
        for e in step:
            if conflicts[e.getDest(step[e])] == 1:
                e.move(step[e])
                if step[e] != '.':
                    converged = False
            else:
                e.move('.')
            coords.append(e.pos)
    
    return it


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