import re

input_filename = 'input.txt'

opponent_map = {'A':1, 'B':2, 'C':3}
yours_map = {'X':1, 'Y':2, 'Z':3}

with open(input_filename, 'r') as f:
    tot = 0
    for line in f.readlines():
        line = line.strip()
        match = re.match(r'(.) (.)', line)

        x,y = opponent_map[match.group(1)], yours_map[match.group(2)]
        tot = tot + y + (6 if y==x%3+1 else 3 if x==y else 0)
    
    print(tot)