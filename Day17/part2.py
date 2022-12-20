debug = 1514285714288

debug_filename = 'debug.txt'
input_filename = 'input.txt'

ITER = 1000000000000
WIDTH = 7

class Chamber:
    def __init__(self, directions):
        self.directions = directions
        self.shapes = [
            [(4,2),(4,3),(4,4),(4,5)],
            [(6,3),(5,2),(5,3),(5,4),(4,3)],
            [(6,4),(5,4),(4,2),(4,3),(4,4)],
            [(7,2),(6,2),(5,2),(4,2)],
            [(5,2),(5,3),(4,2),(4,3)]]

        self.reset()

    
    def copy(self):
        return Chamber(self.directions)

    def reset(self):
        self.height = 0
        self.data = ['.'*WIDTH]
        self.dirIdx = 0
        self.shapeIdx = 0

    def print(self, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = self.height

        for i in range(end, start-1, -1):
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
    return Chamber(f.read())


def doublecheck(chamber, start, delta):
    test = chamber.copy()
    while test.height<start+3*delta:
        test.addRock()
    
    return test.data[start+delta:start+2*delta] == test.data[start+2*delta:start+3*delta]

def findRepetitions(chamber):
    
    patterns = {}

    for it in range(ITER):
        chamber.addRock()
        x = (chamber.dirIdx, chamber.shapeIdx)
        if x not in [patterns[kk]['indexes'] for kk in patterns]:
            patterns[it] = {'indexes': x, 'height': chamber.height}
        else:
            itx = min([kk for kk in patterns.keys() if patterns[kk]['indexes']==x])
            start = patterns[itx]['height']
            delta = chamber.height - start
            if doublecheck(chamber, start, delta):
                return (itx, it), (patterns[itx]['height'], chamber.height)


def solve(chamber):
    reps = findRepetitions(chamber)
    if reps is None:
        return chamber.height
    
    itxs, heights = reps

    deltaIt = itxs[1] - itxs[0]
    deltah = heights[1] - heights[0]

    startit = itxs[0]
    h = heights[0]

    q = (ITER-startit)//deltaIt

    it = startit + q*deltaIt
    h = h + deltah*q - 1
    
    chamber.reset()
    for _ in range(startit+deltaIt):
        chamber.addRock()
    
    buffer = chamber.height

    while it < ITER:
        chamber.addRock()
        it += 1

    h = h + chamber.height - buffer 
    
    return h



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
    
