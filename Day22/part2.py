import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 5031
DIRECTIONS = ['>', 'v', '<', '^']

class CubeFace:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.neighbours = {}
        self.directions = {}
    
    def fix(self):
        for d,n in self.neighbours.items():
            for dd, nn in n.neighbours.items():
                if nn==self:
                    self.directions[d]=rotateLeft(rotateLeft(dd))

    def get(self, x, y):
        return self.data[x][y]

    def getNext(self, x, y, direction):
        face = self
        nx, ny = x, y
        nd = direction
        match direction:
            case '>':
                ny = ny+1
                if ny >= self.size:
                    face, nd = self.neighbours[direction], self.directions[direction]
                    match nd:
                        case '>':
                            ny = 0
                            nx = x
                        case 'v':
                            ny = self.size-x-1
                            nx = 0
                        case '<':
                            ny = self.size-1
                            nx = self.size-x-1
                        case '^':
                            ny = x
                            nx = self.size-1
            case 'v':
                nx = nx+1
                if nx >= self.size:
                    face, nd = self.neighbours[direction], self.directions[direction]
                    match nd:
                        case '>':
                            nx = self.size-y-1
                            ny = 0
                        case 'v':
                            nx = 0
                            ny = y
                        case '<':
                            nx = y
                            ny = self.size-1
                        case '^':
                            ny = self.size-y-1
                            nx = self.size-1
            case '<':
                ny = ny-1
                if ny<0:
                    face, nd = self.neighbours[direction], self.directions[direction]
                    match nd:
                        case '>':
                            ny = 0
                            nx = self.size-x-1
                        case 'v':
                            nx = 0
                            ny = x
                        case '<':
                            ny = self.size-1
                            nx = x
                        case '^':
                            nx = self.size-1
                            ny = self.size-x-1
            case '^':
                nx = nx-1
                if nx < 0:
                    face, nd = self.neighbours[direction], self.directions[direction]
                    match nd:
                        case '>':
                            ny = 0
                            nx = y
                        case 'v':
                            ny = self.size-y
                            nx = 0
                        case '<':
                            ny = self.size-1
                            nx = self.size-y-1
                        case '^':
                            nx = self.size-1
                            ny = y
            case _:
                raise Exception('Invalid direction {}'.format(direction))
                
        if face.get(nx, ny) == '#':
            return self, x, y, direction
        else:
            return face, nx, ny, nd

class MyMap:
    def __init__(self, data):
        size = min([len(x.strip()) for x in data])
        self.size = size
        self.faces = {}
        coords = {}

        for x in range(0, len(data), size):
            for y in range(0, len(data[x]), size):
                d = [x[y:y+size] for x in data[x:x+size]]
                if data[x][y] != ' ':
                    face = CubeFace(d)
                    self.faces[face] = (x,y)
                    coords[(x,y)] = face
        
        def eval(coord, pattern):
            if len(pattern)==0:
                return coord in coords
            else:
                nx, ny = coord
                d = pattern[0]
                if d=='^':
                    nx -= size
                elif d=='>':
                    ny+=size
                elif d=='v':
                    nx+=size
                elif d=='<':
                    ny-=size

                return (coord in coords) and eval((nx, ny), pattern[1:])
        
        def get(coord, pattern):
            if len(pattern)==0:
                return coord
            else:
                nx, ny = coord
                d = pattern[0]
                if d=='^':
                    nx -= size
                elif d=='>':
                    ny+=size
                elif d=='v':
                    nx+=size
                elif d=='<':
                    ny-=size

                return get((nx, ny), pattern[1:])
        
        def getPos(pos, pattern):
            if len(pattern)==0:
                return pos
            d = pattern[0]
            res = d

            if d=='^':
                match pos:
                    case '=':
                        res = 'v'
                    case '.':
                        res = '^'
                    case '<':
                        res = '<'
                    case '^':
                        res = '='
                    case '>':
                        res = '>'
                    case 'v':
                        res = '.'
            elif d=='>':
                match pos:
                    case '=':
                        res = '<'
                    case '.':
                        res = '>'
                    case '<':
                        res = '.'
                    case '^':
                        res = '^'
                    case '>':
                        res = '='
                    case 'v':
                        res = 'v'
            elif d=='v':
                match pos:
                    case '=':
                        res = '^'
                    case '.':
                        res = 'v'
                    case '<':
                        res = '<'
                    case '^':
                        res = '.'
                    case '>':
                        res = '>'
                    case 'v':
                        res = '='
            elif d=='<':
                match pos:
                    case '=':
                        res = '>'
                    case '.':
                        res = '<'
                    case '<':
                        res = '='
                    case '^':
                        res = '^'
                    case '>':
                        res = '.'
                    case 'v':
                        res = 'v'
            
            return getPos(res, pattern[1:])


        for f in self.faces:
            x, y = self.faces[f]
            coord = (x, y)
            visited = []
            
            queue = ['^', '>', 'v', '<']

            while len(queue)>0:
                curr = queue.pop()
                visited.append(get(coord, curr))
                if eval(coord, curr):
                    p = getPos('=', curr)
                    if p in DIRECTIONS:
                        ff = coords[get(coord, curr)]
                        ff.neighbours[p] = f
                    
                    for tmp in '^>v<':
                        if get(coord, curr+tmp) not in visited:
                            queue = [curr+tmp] + queue
        
        for f in self.faces:
            f.fix()

    def getStartingPos(self):
        return list(self.faces.keys())[0], 0, 0, '>'
    
    def getAbsolutePos(self, face, x, y):
        sx, sy = self.faces[face]
        return sx + x, sy + y
    
    def getFaceOf(self, x, y):
        for f in self.faces:
            fx, fy = self.faces[f]
            if fx<=x<fx+self.size and fy<=y<fy+self.size:
                return f
    
    def print(self):
        for x in range(self.size*4):
            line = ''
            for y in range(self.size*4):
                f = self.getFaceOf(x, y)
                if f is None:
                    line += ' '
                else:
                    fx, fy = self.faces[f]
                    line += f.get(x-fx, y-fy)
            print(line)

def getDirectionIdx(dir):
    return min([i for i in range(len(DIRECTIONS)) if DIRECTIONS[i]==dir])
        
def rotateLeft(dir):
    return DIRECTIONS[(getDirectionIdx(dir)-1)%len(DIRECTIONS)]

def rotateRight(dir):
    return DIRECTIONS[(getDirectionIdx(dir)+1)%len(DIRECTIONS)]

def readInput(f):
    data = []
    it = iter(f)
    line = next(it)
    while line.strip()!='':
        data.append(line.replace('\n', ''))
        line = next(it)
    
    m = MyMap(data)

    moves = next(it).strip()
    moves = re.findall(r'((?:\d+)|(?:L|R))', moves)
    
    return m, moves

def solve(model):
    m, moves = model

    face, x, y, dir = m.getStartingPos()

    for move in moves:
        if re.match(r'\d+', move):
            move = int(move)
            for _ in range(move):
                face, x, y, dir = face.getNext(x, y, dir)
        elif move == 'L':
            dir = rotateLeft(dir)
        elif move == 'R':
            dir = rotateRight(dir)
        else:
            raise Exception("Invalid move {}".format(move))

    absolutePos = m.getAbsolutePos(face, x, y)
    idx = getDirectionIdx(dir)
    
    return 1000*(absolutePos[0]+1) + 4*(absolutePos[1]+1) + idx

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