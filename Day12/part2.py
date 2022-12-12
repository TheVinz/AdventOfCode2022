import math

input_filename = "input.txt"

def get_height(c):
    if c=='S':
        return get_height('a')
    elif c=='E':
        return get_height('z')
    else:
        return ord(c)-ord('a')

def is_good_step(a,b,map):
    xa, ya = a
    xb, yb = b

    return 0<=xa<len(map) and 0<=xb<len(map) and 0<=ya<len(map[xa]) and 0<=yb<len(map[xb]) and map[xb][yb]<=map[xa][ya]+1

def walk(s, e, map):
    queue = [[s]]
    closed = [s]

    while len(queue)>0:
        curr = queue.pop()
        a = curr[-1]
        if a==e:
            return curr
        else:
            x,y = a
            for b in [(x+1,y), (x-1,y), (x, y+1), (x, y-1)]:
                if is_good_step(a, b, map) and (b not in closed):
                    queue = [curr + [b]] + queue
                    closed.append(b)
    
    return None



with open(input_filename, 'r') as f:
    data = []
    x = 0
    ss = []
    e = ()

    for line in f:
        line = line.strip()
        l = []
        for y in range(len(line)):
            c = line[y]
            l.append(get_height(c))
            if c=='a':
                ss.append((x,y))
            elif c=='E':
                e = (x,y)
        data.append(l)
        x += 1

    r = math.inf
    i=1

    for s in ss:
        res = walk(s, e, data)
        print('{}/{}'.format(i, len(ss)))
        i+=1
        if res is not None:
            if len(res)-1 < r:
                r=len(res)-1
    print(r)
    

