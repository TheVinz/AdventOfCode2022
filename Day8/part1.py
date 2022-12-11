input_filename = "input.txt"

def visible_top(coord, grid):
    x,y = coord
    value = grid[x][y]

    for i in range(0, x):
        if grid[i][y] >= value:
            return False
    
    return True

def visible_bottom(coord, grid):
    x,y = coord
    value = grid[x][y]

    for i in range(x+1, len(grid)):
        if grid[i][y] >= value:
            return False
    
    return True

def visible_left(coord, grid):
    x,y = coord
    value = grid[x][y]

    for i in range(0, y):
        if grid[x][i] >= value:
            return False
    
    return True

def visible_right(coord, grid):
    x,y = coord
    value = grid[x][y]

    for i in range(y+1, len(grid[x])):
        if grid[x][i] >= value:
            return False
    
    return True

def is_visible(coord, grid):
    return visible_bottom(coord, grid) or visible_left(coord, grid) or visible_right(coord, grid) or visible_top(coord, grid)

with open(input_filename, 'r') as f:
    grid = []
    for line in f.readlines():
        line = line.strip()

        row = []
        for c in line:
            row.append(int(c))
        
        grid.append(row)
    
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if is_visible((x,y), grid):
                res +=1

    print(res)