import re

input_filename = 'input.txt'

point_map = {'A':1, 'B':2, 'C':3}

with open(input_filename, 'r') as f:
    tot = 0
    for line in f.readlines():
        line = line.strip()
        match = re.match(r'(.) (.)', line)

        x,r = point_map[match.group(1)], match.group(2)
        if r=='X':
            # You need to lose
            y = (x-2)%3+1
            p = 0
        elif r=='Y':
            # You need to draw
            y = x
            p = 3
        else:
            # You need to win
            y = x%3+1
            p = 6
        tot = tot + y + p
    
    print(tot)