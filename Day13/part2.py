class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    
    def asList(self):
        left = []
        right = []
        if self.left is not None:
            left = self.left.asList()
        if self.right is not None:
            right = self.right.asList()

        return left + [self.value] + right

    def insert(self, value):
        if compare(self.value, value)<0:
            if self.right is None:
                self.right = Node(value)
            else:
                self.right.insert(value)
        else:
            if self.left is None:
                self.left = Node(value)
            else:
                self.left.insert(value)
            

def compare(a, b):
    if type(a) is int and type(b) is int:
        return -1 if a<b else 0 if a==b else 1
    elif type(a) is list and type(b) is int:
        return compare(a, [b])
    elif type(a) is int and type(b) is list:
        return compare([a], b)
    elif type(a) is list and type(b) is list:
        if len(a)==len(b)==0:
            return 0
        elif len(a)==0:
            return -1
        elif len(b)==0:
            return 1
        else:
            res = compare(a[0], b[0])
            return compare(a[1:], b[1:]) if res==0 else res
            

input_filename = "input.txt"

with open(input_filename, 'r') as f:
    packets = Node([[6]])
    packets.insert([[2]])

    for line in f:
        line = line.strip()
        if line!='':
            packets.insert(eval(line))
    
    p = packets.asList()
    idx = 1
    res = 1

    for p in packets.asList():
        if p==[[2]] or p==[[6]]:
            res *= idx
        idx +=1 

    print(res)
