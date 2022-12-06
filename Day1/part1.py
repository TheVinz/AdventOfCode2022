input_filename = "input.txt"

with open(input_filename, 'r') as f:
    tot = 0
    ans = 0
    for line in f.readlines():
        if line.strip() == '':
            if tot > ans:
                ans = tot
            tot = 0
        else:
            tot += int(line.strip())
    print(ans)