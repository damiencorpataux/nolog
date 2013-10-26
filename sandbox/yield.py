def input(): 
    for i in range(8): yield i

def filter(data):
    c = 1
    s = []
    for i in data:
        s.append(i)
        if c % 2 == 0:
            yield s
            s = []
        c += 1

def output(data):
    for i in data: print i

def wrapinput():
    return input()

output(filter(wrapinput()))

print '--'

i = input()
f = filter(i)
print output(f)
