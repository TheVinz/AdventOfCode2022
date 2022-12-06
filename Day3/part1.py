def priority(c):
    if 'a' <= c <= 'z':
        return ord(c)-ord('a')+1
    elif 'A' <= c <= 'Z':
        return ord(c)-ord('A')+priority('z')+1

def find_match(line):
    fst = line[:len(line)//2]
    snd = line[len(line)//2:]

    elems = [False]*priority('Z')

    for c in fst:
        elems[priority(c)-1]=True
    
    for c in snd:
        if elems[priority(c)-1]:
            return priority(c)

input_filename = 'input.txt'

with open(input_filename, 'r') as f:
    res = 0
    for line in f.readlines():
        res += find_match(line.strip())
    print(res)


