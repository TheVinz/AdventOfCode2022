debug = 3068

debug_filename = 'debug.txt'
input_filename = 'input.txt'

ITER = 2022
WIDTH = 7

class Chamber:
    def __init__(self, file):
        self.height = 0
        self.data = ['.'*WIDTH]


        self.directions = file.read()
        self.dirIdx = 0

        self.shapes = [
            [(4,2),(4,3),(4,4),(4,5)],
            [(6,3),(5,2),(5,3),(5,4),(4,3)],
            [(6,4),(5,4),(4,2),(4,3),(4,4)],
            [(7,2),(6,2),(5,2),(4,2)],
            [(5,2),(5,3),(4,2),(4,3)]]

        self.shapeIdx = 0
    
    def print(self):
        for i in range(len(self.data), -1, -1):
            print(str(i) + (5-len(str(i)))*' ' + '|', end='')
            for j in range(WIDTH):
                print(self.get(i,j), end='')
            print('|')
        print(5*' '+ '+' + '-'*WIDTH + '+')

    def set(self, x, y, c='#'):
        if x<0:
            return

        while self.height<x:
            self.data.append('.'*WIDTH)
            self.height += 1
        

        try:
            old = self.data[x]
        except:
            print("Exception when accessing data with height {}".format(x))
            print("Height: {}".format(self.height))
            print("Data len: {}".format(len(self.data)))

            exit(-1)

        self.data[x] = old[:y] + c + old[y+1:]
    
    def unset(self, x, y):
        old = self.data[x]
        self.data[x] = old[:y] + '.' + old[y+1:]

    def get(self, x, y):
        if x<=0 or y<0 or y>=WIDTH:
            return '#'
        
        if x>self.height:
            return '.'
        
        return self.data[x][y]

    def _nextDir(self):
        res = self.directions[self.dirIdx]
        self.dirIdx = (self.dirIdx+1)%len(self.directions)

        return res

    def _nextShape(self):
        res = self.shapes[self.shapeIdx]
        self.shapeIdx = (self.shapeIdx+1)%len(self.shapes)

        return res

    def fall(self, rock):
        res = []
        
        for x in rock:
            i,j = x
            res.append((i-1, j))
        
        return res

    def canMove(self, rock, direction):
        for x in rock:
            i, j = x
            if direction=='<':
                j = j-1
            elif direction=='>':
                j = j+1
            elif direction=='v':
                i = i-1
            else:
                raise Exception("Invalid direction {}".format(direction))
            
            if self.get(i,j)=='#':
                return False
        
        return True

    def move(self, rock):
        direction = self._nextDir()

        if not self.canMove(rock, direction):
            return rock

        res = []

        for x in rock:
            i,j = x
            if direction=='<':
                j = max(0, j-1)
            elif direction=='>':
                j = min(WIDTH-1, j+1)
            else:
                raise Exception("Invalid direction {}".format(direction))
            res.append((i,j))
        
        return res

    def addRock(self):
        rock = self._nextShape()
        rock = [(i+self.height,j) for (i,j) in rock]

        rock = self.move(rock)

        while(self.canMove(rock, 'v')):
            rock = self.fall(rock)
            rock = self.move(rock)
        
        for (i,j) in rock:
            self.set(i,j)

def readInput(f):
    return Chamber(f)

def solve(chamber):
    for _ in range(ITER):
        chamber.addRock()
    
    return chamber.height


if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        chamber = readInput(f)
    
    res = solve(chamber)
    if res == debug:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(debug, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        chamber = readInput(f)
    print(solve(chamber))
    
    
