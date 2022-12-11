import re

def extract_data(line):
    match = re.match(r'([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)', line)
    return (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))

def is_totally_included(a, b):
    x1, y1 = a
    x2, y2 = b
    
    return (x1>=x2 and y1<=y2) or (x2>=x1 and y2<=y1)

input_filename = 'input.txt'

with open(input_filename, 'r') as f:
    res = 0
    for line in f.readlines():
        a, b = extract_data(line.strip())
        if is_totally_included(a,b):
            res += 1
    print(res)