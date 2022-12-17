def compare(a, b):
    if type(a) is int and type(b) is int:
        return -1 if a<b else 0 if a==b else 1
    elif type(a) is list and type(b) is int:
        return compare(a, [b])
    elif type(a) is int and type(b) is list:
        return compare([a], b)
    elif type(a) is list and type(b) is list:
        if len(a)==len(b)==0:
            return 0
        elif len(a)==0:
            return -1
        elif len(b)==0:
            return 1
        else:
            res = compare(a[0], b[0])
            return compare(a[1:], b[1:]) if res==0 else res
            

input_filename = "input.txt"

with open(input_filename, 'r') as f:
    packets = {}
    state = 'left'
    idx = 1
    res = 0

    for line in f:
        line = line.strip()
        if line == '':
            state = 'left'
            idx += 1
        else:
            packets[state] = eval(line)
            if state == 'left':
                state = 'right'
            elif state == 'right':
                if compare(packets['left'], packets['right'])==-1:
                    res += idx
    
    print(res)
