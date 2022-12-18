import re
import math

debug = (10, 26)
test = (2000000)

debug_filename = 'debug.txt'
input_filename = 'input.txt'

def manhattanDistance(ax, ay, bx, by):
    return abs(ax-bx) + abs(ay-by)

class Sensor:
    def __init__(self, x, y, closestBeacon):
        self.x = x
        self.y = y
        self.closestBeacon = closestBeacon

class Beacon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SensorsMap:
    def __init__(self, sensors):
        maxx = -math.inf
        maxy = maxx
        minx = math.inf
        miny = minx

        for s in sensors:
            b = s.closestBeacon
            d = manhattanDistance(b.x, b.y, s.x, s.y)

            if s.x+d > maxx:
                maxx = s.x+d
            if s.x-d < minx:
                minx = s.x-d
            if s.y+d > maxy:
                maxy = s.y+d
            if s.y-d < miny:
                miny = s.y-d

        self.rangex = (minx, maxx+1)
        self.rangey = (miny, maxy+1)
        self.sensors = sensors

    def check(self, x, y):
        for s in self.sensors:
            b = s.closestBeacon
            if (x,y) == (s.x, s.y) or (x,y) == (b.x, b.y):
                return 0
        
        for s in self.sensors:
            b = s.closestBeacon
            if manhattanDistance(x,y,s.x,s.y) <= manhattanDistance(b.x, b.y, s.x, s.y):
                return 1
        
        return 0

    def solve(self, y):
        res = 0
        for x in range(self.rangex[0], self.rangex[1]):
            res += self.check(x, y)
        return res

def init(f):
    sensors = []

    for line in f:
        line = line.strip()
        match = re.findall(r'=([-]?\d+)', line)
        match = [int(x) for x in match]
        sensors.append(Sensor(match[0], match[1], Beacon(match[2], match[3])))
    
    return SensorsMap(sensors)


if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        m = init(f)
        
        res = m.solve(debug[0])
        if res == debug[1]:
            print("Debug test passed, running on probelm input...")
        else:
            print("Debug test failed.\nExpected output: {}\nActual output: {}".format(debug[1], res))
            exit(-1)

    with open(input_filename, 'r') as f:
        m = init(f)
        print(m.solve(test))

        