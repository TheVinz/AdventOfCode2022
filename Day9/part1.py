import re

input_filename = "input.txt"

def update_tail(tail_pos, head_pos):
    tx, ty = tail_pos
    hx, hy = head_pos

    x,y = tail_pos

    if tx==hx:
        if hy>ty+1:
            y = ty+1
        elif hy<ty-1:
            y = ty-1
    elif ty==hy:
        if hx>tx+1:
            x = tx+1
        elif hx<tx-1:
            x = tx-1
    elif abs(ty-hy)>1 or abs(tx-hx)>1:
        x = tx + abs(hx-tx)//(hx-tx)
        y = ty + abs(hy-ty)//(hy-ty)
    
    return x,y


def update_head(pos, dir):
    x,y = pos
    match dir:
        case 'U':
            x=x+1
        case 'D':
            x=x-1
        case 'L':
            y=y-1
        case 'R':
            y=y+1
        case _:
            raise Exception("Invalid direction")
    
    return x,y


with open(input_filename, 'r') as f:
    head_pos = 0,0
    tail_pos = 0,0

    visited = [tail_pos]
    for line in f.readlines():
        line = line.strip()
        match = re.match(r'([A-Z]) (\d+)', line)

        direction = match.group(1)
        steps = int(match.group(2))

        for _ in range(steps):
            head_pos = update_head(head_pos, direction)
            tail_pos = update_tail(tail_pos, head_pos)

            if tail_pos not in visited:
                visited.append(tail_pos)

    print(len(visited))

