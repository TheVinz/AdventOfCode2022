import re

input_filename = "input.txt"

LEN_ROPE = 10

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
    rope = [(0,0) for _ in range(LEN_ROPE)]    

    visited = [rope[-1]]
    for line in f.readlines():
        line = line.strip()
        match = re.match(r'([A-Z]) (\d+)', line)

        direction = match.group(1)
        steps = int(match.group(2))

        for _ in range(steps):
            rope[0] = update_head(rope[0], direction)

            for i in range(1, len(rope)):
                rope[i] = update_tail(rope[i], rope[i-1])

            if rope[-1] not in visited:
                visited.append(rope[-1])

    print(len(visited))

