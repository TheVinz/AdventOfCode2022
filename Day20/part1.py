debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 3
PLACEHOLDER = 1000
COORDS = 3

class Node:
    def __init__(self, val):
        self.before = self
        self.after = self
        self.value = val
    
    def insertBefore(self, node):
        if node==self:
            raise Exception("Trying to insert node before itself")

        node.unlink()

        b = self.before
        self.before = node
        b.after = node

        node.before = b
        node.after = self

    def insertAfter(self, node):
        if node==self:
            raise Exception("Trying to insert node after itself")

        node.unlink()

        a = self.after
        self.after = node
        a.before = node

        node.after = a
        node.before = self
    
    def unlink(self):
        self.before.after = self.after
        self.after.before = self.before

        self.before = self
        self.after = self


def readInput(f):
    res = []
    for line in f:
        line = line.strip()
        val = int(line)
        node = Node(val)
        if len(res)>0:
            res[-1].insertAfter(node)
        res.append(node)

    return res

def solve(model: list):
    for n in model:
        if n.value < 0:
            tmp = n
            for _ in range(-n.value%(len(model)-1)):
                tmp = tmp.before
            tmp.before.insertAfter(n)
        elif n.value > 0:
            tmp = n
            for _ in range(n.value%(len(model)-1)):
                tmp = tmp.after
            tmp.after.insertBefore(n)

    n = model[0]
    while n.value != 0:
        n=n.after
    
    res = 0
    
    for _ in range(COORDS):
        for _ in range(PLACEHOLDER%len(model)):
            n=n.after
        res += n.value
    
    return res

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