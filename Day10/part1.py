import re

input_filename = "input.txt"
CHECKPOINTS = range(20, 221, 40)

class Counter:
    def __init__(self):
        self.res = 0
        self.cycle = 0
        self.x = 1
    
    def _cycle(self):
        self.cycle += 1
        if self.cycle in CHECKPOINTS:
            self.res += self.cycle * self.x

    def noop(self):
        self._cycle()
    
    def addx(self, val):
        self._cycle()
        self._cycle()

        self.x += val

with open(input_filename, 'r') as f:
    state = Counter()

    for line in f.readlines():
        line = line.strip()

        if line=='noop':
            state.noop()
        else:
            increase = int(re.match(r'addx ([-]?\d+)', line).group(1))
            state.addx(increase)


    print(state.res)

