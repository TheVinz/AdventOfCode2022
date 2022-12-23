import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 152

class Monkey:
    def __init__(self, string):
        self.string = string
        self.hasVal = False
    
    def link(self, monkeys):
        if re.match(r'[-]?\d+', self.string):
            self.val = int(self.string)
            self.hasVal = True
        else:
            match = re.match(r'(\w+) ([+-/*]) (\w+)', self.string)
            self.children = monkeys[match.group(1)], monkeys[match.group(3)]
            self.op = match.group(2)
    
    def getVal(self):
        if not self.hasVal:
            a, b = self.children
            a = a.getVal()
            b = b.getVal()

            self.val = eval('{} {} {}'.format(a, self.op, b))
            self.hasVal = True
        
        return self.val
            

def readInput(f):
    model = {}

    for line in f:
        line = line.strip()
        name, string = line.split(': ')
        model[name] = Monkey(string)
    
    for m in model.values():
        m.link(model)
    
    return model

def solve(model):
    return int(model['root'].getVal())

if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        model = readInput(f)
    res = solve(model)
    print(res)

    if res == DEBUG:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(DEBUG, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        model = readInput(f)
    print(solve(model))