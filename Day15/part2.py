import re

debug = (20, 56000011)
test = (4000000)

debug_filename = 'debug.txt'
input_filename = 'input.txt'

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def manhattanDistance(self, other) -> int:
        return abs(self.x-other.x) + abs(self.y-other.y)


class Sensor(Point):
    def __init__(self, x: int, y: int, closestBeacon: Point):
        super().__init__(x, y)
        
        self.range = self.manhattanDistance(closestBeacon)

    def contains(self, point: Point) -> bool:
        return self.manhattanDistance(point) <= self.range

class SensorsMap:
    def __init__(self, sensors: list):
        self.sensors = sensors

    def check(self, p: Point) -> list:
        return [s for s in self.sensors if s.contains(p)]
        
    def solve(self, m: int) -> int:
        for x in range(0, m+1):
            y=0
            while y<=m:
                p=Point(x, y)
                ss = self.check(p)
                if len(ss) == 0:
                    print("Found {},{}".format(x,y))
                    return x*4000000+y
                else:
                    y = max([s.range-abs(s.x-x)+s.y for s in ss]) + 1
                                    
        raise Exception("No feasible point found")

def init(f):
    sensors = []

    for line in f:
        match = [int(x) for x in re.findall(r'=([-]?\d+)', line.strip())]
        sensors.append(Sensor(match[0], match[1], Point(match[2], match[3])))
    
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

        