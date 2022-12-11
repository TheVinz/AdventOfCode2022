import re

input_filename = "input.txt"
LEN_LINE = 40

class Renderer:
    def __init__(self):
        self.cycle = 0
        self.x = 1
        self._data = ['' for _ in range(240)]
    
    def _cycle(self):
        self.cycle += 1
        sprite = (self.x-1, self.x, self.x+1)

        print(self.x, self.cycle)

        self._data[self.cycle-1] = '#' if (self.cycle-1)%LEN_LINE in sprite else '.'


    def noop(self):
        self._cycle()
    
    def addx(self, val):
        self._cycle()
        self._cycle()

        self.x += val
    
    def show(self):
        acc = ''
        for c in self._data:
            acc = acc+c
            if len(acc)==LEN_LINE:
                print(acc)
                acc=''
        

with open(input_filename, 'r') as f:
    state = Renderer()

    for line in f.readlines():
        line = line.strip()

        if line=='noop':
            state.noop()
        else:
            increase = int(re.match(r'addx ([-]?\d+)', line).group(1))
            state.addx(increase)


    state.show()

