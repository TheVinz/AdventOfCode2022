import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 301
ROOT = 'root'
HUMAN = 'humn'

class Monkey:
    def __init__(self, string):
        self.string = string
        self.hasVal = False
    
    def link(self, monkeys):
        if re.match(r'[-]?\d+', self.string):
            self.val = int(self.string)
            self.hasVal = True
        elif self.string==HUMAN:
            self.val = HUMAN
            self.hasVal = True
        else:
            match = re.match(r'(\w+) ([+\-\/*]|=) (\w+)', self.string)

            a = match.group(1)
            b = match.group(3)

            a = monkeys[a]
            b = monkeys[b]

            self.children = a, b
            self.op = match.group(2)
    
    def getVal(self):
        if not self.hasVal:
            a, b = self.children

            if a!=HUMAN:
                a = a.getVal()
            if b!=HUMAN:
                b = b.getVal()

            self.val = '({} {} {})'.format(a, self.op, b)
            if HUMAN not in self.val:
                self.val = eval(self.val)

            self.hasVal = True
        
        return self.val
    
    def solve(self, term):
        if self.getVal() == HUMAN:
            return term
        a,b = self.children
        
        op = self.op

        match self.op:
            case '+':
                op = '-'
            case '-':
                op = '+'
            case '*':
                op = '/'
            case '/':
                op = '*'
            case _:
                raise Exception('Invalid operation {}'.format(self.op))

        if type(a.getVal()) is str:
            tmp = '{} {} {}'.format(term, op, b.getVal())
            return a.solve(eval(tmp))
        elif type(b.getVal()) is str:
            if op == '+':
                tmp = '{} {} {}'.format(a.getVal(), '-', term)
            elif op == '*':
                tmp = '{} {} {}'.format(a.getVal(), '/', term)
            else:
                tmp = '{} {} {}'.format(term, op, a.getVal())
            return b.solve(eval(tmp))
        else:
            raise Exception('Something went wrong...')

            

def readInput(f):
    model = {}

    for line in f:
        line = line.strip()
        name, string = line.split(': ')
        if name == HUMAN:
            model[name] = Monkey(HUMAN)
        elif name == ROOT:
            match = re.match(r'\w+ (.) \w+', string)
            string = string.replace(match.group(1), '=')
            model[name] = Monkey(string)
        else:
            model[name] = Monkey(string)
    
    for m in model.values():
        m.link(model)
    
    return model

def solve(model):
    a, b = model[ROOT].children
    if HUMAN in a.getVal():
        return int(a.solve(b.getVal()))
    else:
        return int(b.solve(a.getVal()))
    

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