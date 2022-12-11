import re

def extract_data(line):
    match = re.match(r'([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)', line)
    return (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))

def is_overlap(a, b):
    x1, y1 = a
    x2, y2 = b
    
    return not (x1>y2 or x2>y1)

input_filename = 'input.txt'

with open(input_filename, 'r') as f:
    res = 0
    for line in f.readlines():
        a, b = extract_data(line.strip())
        if is_overlap(a,b):
            res += 1
            print(line.strip())
    print(res)