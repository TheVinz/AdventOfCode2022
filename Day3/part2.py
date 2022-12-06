def priority(c):
    if 'a' <= c <= 'z':
        return ord(c)-ord('a')+1
    elif 'A' <= c <= 'Z':
        return ord(c)-ord('A')+priority('z')+1

def find_match(fst, snd, trd):

    elems_fst = [False]*priority('Z')
    elems_snd = [False]*priority('Z')
    elems_trd = [False]*priority('Z')

    for c in fst:
        elems_fst[priority(c)-1] = True
    
    for c in snd:
        elems_snd[priority(c)-1] = True

    for c in trd:
        elems_trd[priority(c)-1] = True
        
    for prio in range(0, priority('Z')):
        if elems_fst[prio] and elems_snd[prio] and elems_trd[prio]:
            return prio+1


input_filename = 'input.txt'

with open(input_filename, 'r') as f:
    res = 0
    group = []
    for line in f.readlines():
        group.append(line.strip())
        if len(group) == 3:
            res += find_match(*group)
            group = []
    print(res)


