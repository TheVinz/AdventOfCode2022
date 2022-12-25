debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = '2=-1=0'

def snafu2dec(snafu):
    if len(snafu)==0:
        return 0
    if len(snafu)==1:
        match snafu:
            case '2':
                return 2
            case '1':
                return 1
            case '0':
                return 0
            case '-':
                return -1
            case '=':
                return -2

    p = 1
    res = 0
    for d in reversed(snafu):
        res += p*snafu2dec(d)
        p*=5
    return res

def dec2five(n):
    s = ""
    while n:
        s = str(n % 5) + s
        n = n//5
    return s
    
def plusone(snafu):
    if len(snafu)==0:
        return '1'
    if len(snafu)==1:
        res = ['=', '-', '0', '1', '2', '1=']
        for i in range(len(res)):
            if res[i]==snafu:
                return res[(i+1)]
    
    a, b = snafu[:-1], snafu[-1]

    b = plusone(b)
    if b=='1=':
        return plusone(a) + '='
    else:
        return a+b
    

def dec2snafu(dec):
    res = ''
    for i in dec2five(dec):
        if i=='4':
            res = plusone(res)+'-'
        elif i=='3':
            res = plusone(res)+'='
        else:
            res = res+i
    return res    

def readInput(f):
    model = []
    for line in f:
        model.append(line.strip())
    return model

def solve(model):
    res = 0

    for x in model:
        res += snafu2dec(x)
    return dec2snafu(res)

if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        model = readInput(f)
    res = solve(model)

    if res == DEBUG:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(DEBUG, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        model = readInput(f)
    print(solve(model))