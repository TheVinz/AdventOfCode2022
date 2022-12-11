import re

MOD = 96577

class Parser():
    def __init__(self):
        self.monkeys = {}
        self.current = None
    
    def parse(self, line):
        if re.match(r'Monkey (?:\d+):', line):
            self.current = int(re.match(r'Monkey (\d+)', line).group(1))
            self.monkeys[self.current] = Monkey()
        elif "Starting items" in line:
            items = list(map(lambda x : int(x), re.findall(r'(?: (\d+))', line)))
            self.monkeys[self.current].setItems(items)
        elif "Operation" in line:
            op = re.findall(r'new = (.*)$', line)[0]
            self.monkeys[self.current].setOp(op)
        elif "Test" in line:
            test = int(re.findall(r'(\d+)', line)[0])
            self.monkeys[self.current].setTest(test)
        elif "If true" in line:
            self.monkeys[self.current].setOptionOne(int(re.findall(r'(\d+)', line)[0]))
        elif "If false" in line:
            self.monkeys[self.current].setOptionTwo(int(re.findall(r'(\d+)', line)[0]))

    def getMonkeys(self):
        return self.monkeys



class Monkey():
    def __init__(self):
        self.processed = 0

    def setItems(self, items):
        self.items = items
    
    def setOp(self, op):
        self.op = op

    def setTest(self, test):
        self.test = test

    def setOptionOne(self, option):
        self.optionOne = option
    
    def setOptionTwo(self, option):
        self.optionTwo = option

    def examine(self):
        old = self.items.pop()
        new = eval(self.op)%MOD
        self.processed += 1

        if not new%self.test:
            return new, self.optionOne
        else:
            return new, self.optionTwo

    def enqueue(self, item):
        self.items = [item, *self.items]
    
    def print(self):
        print("Starting items: {}".format(self.items))
        print("Operation: new = {}".format(self.op))
        print("Test: divisible by {}".format(self.test))
        print("  If true: throw to monkey {}".format(self.optionOne))
        print("  If false: throw it to monkey {}".format(self.optionTwo))

input_filename = "input.txt"

with open(input_filename, 'r') as f:

    parser = Parser()

    for line in f.readlines():
        line = line.strip()
        parser.parse(line)
    
    monkeys = parser.getMonkeys()

    for _ in range(10000):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            while len(monkey.items)>0:
                item, idx = monkey.examine()
                monkeys[idx].enqueue(item)
    
    processed = [m.processed for _,m in monkeys.items()]
    print(processed)
    processed.sort()
    print(processed[-2]*processed[-1])
        

        