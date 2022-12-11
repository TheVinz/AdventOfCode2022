import re

input_filename = "input.txt"

def parse_input(line, data):
    regex = r'((?:   |\[[A-Z]\]))(?: |$)'
    res = []

    matches = re.finditer(regex, line)

    for match in matches:
        res.append(match.group(1).replace(' ', '').replace('[','').replace(']',''))
    
    for i in range(len(res)):
        if (i+1) not in data:
            data[i+1] = []
        data[i+1] = ([res[i]] if res[i]!='' else []) + data[i+1]

    return data

def execute(line, data):
    regex = r'move (\d+) from (\d+) to (\d+)'

    match = re.match(regex, line)
    move = int(match.group(1))
    frm = int(match.group(2))
    to = int(match.group(3))
    
    for _ in range(move):
        x = data[frm].pop()
        data[to].append(x)

    return data


with open(input_filename, 'r') as f:
    init = True
    data = {}
    for line in f.readlines():

        if init:
            if line.strip() == '':
                init=False
            else:
                data = parse_input(line, data)
        else:
            data = execute(line.strip(), data)

    print(''.join([data[i][-1] for i in data]))