input_filename = "input.txt"

def scenic_score_top(coord, grid):
    x,y = coord
    value = grid[x][y]

    res=0

    for i in range(x-1, -1, -1):
        res+=1
        if grid[i][y]>=value:
            return res
    
    return res
        

def scenic_score_bottom(coord, grid):
    x,y = coord
    value = grid[x][y]

    res=0

    for i in range(x+1, len(grid)):
        res+=1
        if grid[i][y]>=value:
            return res
    
    return res

def scenic_score_left(coord, grid):
    x,y = coord
    value = grid[x][y]

    res=0

    for i in range(y-1, -1, -1):
        res+=1
        if grid[x][i]>=value:
            return res
    
    return res

def scenic_score_right(coord, grid):
    x,y = coord
    value = grid[x][y]

    res=0

    for i in range(y+1, len(grid[x])):
        res+=1
        if grid[x][i]>=value:
            return res
    
    return res

def scenic_score(coord, grid):
    return scenic_score_top(coord, grid)*scenic_score_bottom(coord, grid)*scenic_score_left(coord, grid)*scenic_score_right(coord, grid)

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
            tmp = scenic_score((x,y), grid)
            if tmp>res:
                res=tmp

    print(res)