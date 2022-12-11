import re
import math

FILE = 0
DIR = 1

SIZE_TOT = 70000000
SIZE_UPDATE = 30000000

class Node:
    def __init__(self, type, name=None, parent=None, size=0):
        self.type = type
        self._size = size
        self.name = name
        self.parent=parent
        if type==DIR:
            self._children = []
    
    def addChild(self, child):
        if self.type == FILE:
            raise Exception('Adding children to a file')
        
        if not self.hasChild(child.name):
            self._children.append(child)
    
    def children(self):
        if self.type == FILE:
            raise Exception("Trying to access file's children")
        return self._children.copy()
    
    def hasChild(self, name):
        if self.type == FILE:
            return False

        for i in self._children:
            if i.name==name:
                return True

        return False            

    def find(self, name):
        if self.type == FILE:
            raise Exception("Finding into a file")
        for c in self._children:
            if c.name == name:
                return c

        raise Exception("Children {} not found in {}".format(name, self.name))

    def size(self):
        if self.type==FILE:
            return self._size
        else:
            return sum(map(lambda x: x.size(), self._children))

    def print(self, level=0):
        if self.type==FILE:
            print('  '*level + '- {} (file, size={})'.format(self.name, self._size))
        else:
            print('  '*level+'- {} (dir)'.format(self.name))
            for c in self._children:
                c.print(level+1)

    def solve(self, threshold):
        if self.type == FILE:
            return math.inf
        
        size = self.size()

        if size >= threshold:
            return min([size] + [x.solve(threshold) for x in self._children])
        else:
            return min([x.solve(threshold) for x in self._children] + [math.inf])

    
    

input_filename = "input.txt"

with open(input_filename, 'r') as f:

    root = Node(DIR, 'root')
    current_dir = Node(DIR, None)

    for line in f.readlines():
        line = line.strip()
        if line.startswith('$'):
            if 'cd' in line:
                if line == '$ cd /':
                    current_dir = root
                elif line == '$ cd ..':
                    current_dir = current_dir.parent
                else:
                    name = re.match(r'\$ cd ((?:\w|[-.])+)', line).group(1)
                    current_dir = current_dir.find(name)
        else:
            if 'dir' in line:
                name = re.match(r'dir ((?:\w|[.-])+)', line).group(1)
                current_dir.addChild(Node(DIR, name, current_dir))
            else:
                match = re.match(r'(\d+) ((?:\w|[.-])+)', line)

                size = int(match.group(1))
                name = match.group(2)

                current_dir.addChild(Node(FILE, name, current_dir, size))
    
    root_size = root.size()
    free_space = SIZE_TOT - root_size
    to_free = SIZE_UPDATE - free_space

    print("Root size: {}\nFree space: {}\nSpace to be freed for update: {}\nSolution: {}".format(root_size, free_space, to_free, root.solve(to_free)))


