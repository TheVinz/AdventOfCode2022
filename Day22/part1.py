import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 6032

class DirectionsIter:
    def __init__(self):
        self.directions = ['>', 'v', '<', '^']
        self.idx = 0
    
    def left(self):
        self.idx = (self.idx-1)%len(self.directions)
        return self.directions[self.idx]
    
    def right(self):
        self.idx = (self.idx+1)%len(self.directions)
        return self.directions[self.idx]
    
    def start(self):
        self.idx = 0
        return self.directions[self.idx]

class MyMap:
    def __init__(self):
        self.data = []
        self.lines = []
        self.columns = []
    
    def append(self, line):
        lineIdx = len(self.data)
        self.data.append(line.strip())

        start = 0
        it = iter(line)

        while next(it)==' ':
            start += 1

        self.lines.append((start, len(line)))
        while len(self.columns)<start:
            self.columns = [None] + self.columns

        for start in range(start, len(line)):
            if len(self.columns)==start:
                self.columns.append((lineIdx, lineIdx+1))
            elif self.columns[start] is None:
                self.columns[start] = (lineIdx, lineIdx+1)
            else:
                cs, _ = self.columns[start]
                self.columns[start] = (cs, lineIdx+1)
    
    def get(self, x, y):
        if x<0 or x>=len(self.lines) or y<0 or y>=len(self.columns):
            return ' '

        ls, le = self.lines[x]
        cs, _ = self.columns[y]

        if ls<=y<le:
            return self.data[x][y-ls]
        else: 
            return ' '
    
    def getNext(self, x, y, direction):
        nx, ny = x,y

        match direction:
            case '>':
                ny = ny+1
                sl, el = self.lines[nx]
                if ny >= el:
                    ny = sl
            case 'v':
                nx = nx+1
                sc, ec = self.columns[ny]
                if nx >= ec:
                    nx = sc
            case '<':
                ny = ny-1
                sl, el = self.lines[nx]
                if ny < sl:
                    ny = el-1
            case '^':
                nx = nx-1
                sc, ec = self.columns[ny]
                if nx < sc:
                    nx = ec-1
            case _:
                raise Exception('Invalid direction {}'.format(direction))
        
        if self.get(nx, ny) != '#':
            return nx, ny
        else:
            return x,y

    
    def getStartingPos(self):
        return 0, self.lines[0][0]
    
    def print(self):
        for x in range(len(self.lines)):
            for y in range(len(self.columns)):
                print(self.get(x, y), end='')
            print()


def readInput(f):
    m = MyMap()
    it = iter(f)
    line = next(it)
    while line.strip()!='':
        m.append(line.replace('\n', ''))
        line = next(it)

    moves = next(it).strip()
    moves = re.findall(r'((?:\d+)|(?:L|R))', moves)
    
    return m, moves

def solve(model):
    m, moves = model
    directionsIter = DirectionsIter()

    direction = directionsIter.start()
    pos = m.getStartingPos()

    for move in moves:
        if re.match(r'\d+', move):
            move = int(move)
            for _ in range(move):
                pos = m.getNext(*pos, direction)
        elif move == 'L':
            direction = directionsIter.left()
        elif move == 'R':
            direction = directionsIter.right()
        else:
            raise Exception("Invalid move {}".format(move))
    
    return 1000*(pos[0]+1) + 4*(pos[1]+1) + directionsIter.idx

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