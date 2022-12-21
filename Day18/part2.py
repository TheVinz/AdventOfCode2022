import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

debug = 58

class Point:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    
    def __str__(self):
        return str((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y and self.z==other.z

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
        
        self.minx -=1
        self.maxx +=1
        self.miny -=1
        self.maxy +=1
        self.minz -=1
        self.maxz +=1

        self.data = [0]*(self.maxz - self.minz+1)*(self.maxy-self.miny+1)*(self.maxx-self.minx+1)

        for p in points:
            self.set(p, 1)

    
    def get(self, p):
        if p.x < self.minx or p.x>self.maxx or p.y < self.miny or p.y > self.maxy or p.z < self.minz or p.z>self.maxz:
            return -1
        
        idx = (p.x-self.minx)*(self.maxy-self.miny+1)*(self.maxz-self.minz+1) + (p.y-self.miny)*(self.maxz-self.minz+1) + (p.z-self.minz)
        return self.data[idx]
    
    def set(self, p, val):
        if p.x < self.minx or p.x>self.maxx or p.y < self.miny or p.z>self.maxz or p.z < self.minz or p.z>self.maxz:
            return

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

def neighbours(point):
    x = point.x
    y = point.y
    z = point.z

    return [Point(x+1,y,z), Point(x-1,y,z), Point(x,y+1,z), Point(x,y-1,z), Point(x,y,z+1), Point(x,y,z-1)]

def fill(droplet):
    queue = [Point(droplet.minx, droplet.miny, droplet.minz)]

    while len(queue)>0:
        point = queue.pop()
        droplet.set(point, -1)
        
        for p in neighbours(point):
            if droplet.get(p)==0 and p not in queue:
                queue = [p] + queue

def canReach(droplet, source, visited):
    print([str(x) for x in visited])
    if droplet.get(source)==-1:
        return True
    if droplet.get(source)==1:
        return False
    
    res = sum([canReach(droplet, n, [*visited, source]) for n in neighbours(source) if n not in visited])

    return res==1

def solve(droplet, points):
    fill(droplet)
    
    res = 0
    for p in points:
        for i in neighbours(p):
            if droplet.get(i)==-1:
                res+=1
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
