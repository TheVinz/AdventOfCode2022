import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

debug = 64

class Point:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z

class Droplet:
    def __init__(self, points):
        self.maxx = -10e7
        self.minx = -self.maxx
        self.maxy = self.maxx
        self.miny = self.minx
        self.maxz = self.maxx
        self.minz = self.minx
        for p in points:
            if p.x > self.maxx:
                self.maxx = p.x
            if p.x < self.minx:
                self.minx = p.x
            if p.y > self.maxy:
                self.maxy = p.y
            if p.y < self.miny:
                self.miny = p.y
            if p.z > self.maxz:
                self.maxz = p.z
            if p.z < self.minz:
                self.minz = p.z

        self.data = [0]*(self.maxz - self.minz+1)*(self.maxy-self.miny+1)*(self.maxx-self.minx+1)

        for p in points:
            self.set(p, 1)

    
    def get(self, p):
        if p.x < self.minx or p.x>self.maxx or p.y < self.miny or p.y > self.maxy or p.z < self.minz or p.z>self.maxz:
            return 0
        
        idx = (p.x-self.minx)*(self.maxy-self.miny+1)*(self.maxz-self.minz+1) + (p.y-self.miny)*(self.maxz-self.minz+1) + (p.z-self.minz)
        return self.data[idx]
    
    def set(self, p, val):
        if p.x < self.minx or p.x>self.maxx or p.y < self.miny or p.z>self.maxz or p.z < self.minz or p.z>self.maxz:
            raise Exception('Index our of bound: ({}, {}, {})'.format(p.x, p.y, p.z))

        idx = (p.x-self.minx)*(self.maxy-self.miny+1)*(self.maxz-self.minz+1) + (p.y-self.miny)*(self.maxz-self.minz+1) + (p.z-self.minz)
        self.data[idx] = val
            


def readInput(f):
    points = []
    for line in f:
        line = line.strip()
        matches = re.findall(r'([-]?\d+)', line)
        p = Point(int(matches[0]), int(matches[1]), int(matches[2]))
        points.append(p)

    return Droplet(points), points


def solve(droplet, points):
    res = 0
    for p in points:
        if droplet.get(Point(p.x+1, p.y, p.z)) == 0:
            res += 1
        if droplet.get(Point(p.x-1, p.y, p.z)) == 0:
            res += 1
        if droplet.get(Point(p.x, p.y+1, p.z)) == 0:
            res += 1
        if droplet.get(Point(p.x, p.y-1, p.z)) == 0:
            res += 1
        if droplet.get(Point(p.x, p.y, p.z+1)) == 0:
            res += 1
        if droplet.get(Point(p.x, p.y, p.z-1)) == 0:
            res += 1
    return res


if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        droplet, points = readInput(f)
    res = solve(droplet, points)

    if res == debug:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(debug, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        droplet, points = readInput(f)
    print(solve(droplet, points))
