import re

class MyMap:
    def __init__(self, segments, max_y, max_x, min_x):
        self.data = [['.' for _ in range(max_y+3)] for _ in range(max_x-min_x+1)]

        self.range = (min_x, max_x)

        segments.append([(min_x, max_y+2), (max_x, max_y+2)])

        self.set(500, 0, 'x')

        for s in segments:
            prev = s[0]
            for curr in s[1:]:
                self.drawLine(prev, curr)
                prev=curr
        
    def fix(self, x):
        line = ['.' for _ in range(len(self.data[0]))]
        line[-1] = '#'

        while x<=self.range[0]:
            self.range = self.range[0]-1, self.range[1]
            self.data = [line] + self.data
        while x>=self.range[1]:
            self.range = self.range[0], self.range[1]+1
            self.data.append(line)

    def set(self, x, y, val):
        self.data[x-self.range[0]][y] = val
    
    def get(self, x, y):
        return self.data[x-self.range[0]][y]
    
    def print(self):
        for x in range(self.range[0], self.range[1]+1):
            for y in range(len(self.data[x-self.range[0]])):
                print(self.get(x, y), end='')
            print('')
    
    def drawLine(self, a, b):
        if a[0] == b[0]:
            incr = -1 if a[1]>b[1] else 1
            for y in range(a[1], b[1]+incr, incr):
                self.set(a[0], y, '#')
        elif a[1] == b[1]:
            incr =  -1 if a[0]>b[0] else 1
            for x in range(a[0], b[0]+incr, incr):
                self.set(x, a[1], '#')
        else:
            raise Exception("Cannot draw diagonal line")

    def fall(self, x, y):
        if x<=self.range[0] or x>=self.range[1]:
            self.fix(x)

        if self.get(x,y+1) == '.':
            return x, y+1
        elif self.get(x-1, y+1) == '.':
            return x-1, y+1
        elif self.get(x+1, y+1) == '.':
            return x+1, y+1
        else:
            return x,y
    
    def drop(self):
        x,y = 500, 0

        while self.fall(x,y) != (x,y):
            x, y = self.fall(x,y)
        
        self.set(x,y,'o')
        return (x,y) != (500,0)
        

    

input_filename = "input.txt"

with open(input_filename, 'r') as f:
    segments = []
    max_y = 0
    min_x = 500
    max_x = 500

    for line in f:
        line = line.strip()
        matches = re.findall(r'(\d+,\d+)(?: -> |$)', line)
        seg = []
        for m in matches:
            x, y = eval(m)

            if x<min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

            seg.append((x,y))

        segments.append(seg)

    m = MyMap(segments, max_y, max_x, min_x)
    cnt = 0

    while m.drop():
        cnt = cnt+1
    
    print(cnt+1)