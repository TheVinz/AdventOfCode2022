input_filename = "input.txt"

with open(input_filename, 'r') as f:
    tot = 0
    totals = []
    for line in f.readlines():
        if line.strip() == '':
            totals.append(tot)
            tot = 0
        else:
            tot += int(line.strip())
    totals.sort()            
    print(sum(totals[-3:]))