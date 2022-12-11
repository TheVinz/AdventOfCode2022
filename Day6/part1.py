input_filename = "input.txt"   
window_size = 4 

def sum_cache(cache):
    return sum(map(lambda x: 1 if x>0 else 0, cache))

def char2index(c):
    return ord(c)-ord('a')

def solve(data):
    cache = [0 for _ in range(ord('z')-ord('a')+1)]
    s = data[0:window_size]
    for c in s:
        cache[char2index(c)] += 1
    
    if  sum_cache(cache) == window_size:
        return window_size

    for i in range(window_size, len(data)):
        cache[char2index(data[i-window_size])] -= 1
        cache[char2index(data[i])] += 1
        if  sum_cache(cache) == window_size:
            return i+1

with open(input_filename, 'r') as f:

    data = f.read()
    print(solve(data))
    