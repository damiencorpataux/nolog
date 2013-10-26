#!/usb/bin/python

def filter(data, count=2):
    stack = []
    for line in data:
        stack.append(line)
        if len(stack) == count:
            join = '\n'.join(stack)
            print 'Stacked: %s' % join 
            stack = []
            yield join
