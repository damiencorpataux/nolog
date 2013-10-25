#!/usb/bin/python

def filter(data, count=2):
    stack = []
    for line in data:
        if len(stack) == count:
            join = '\n'.join(stack)
            yield join
            print 'Stacked: %s' % join 
            stack = []
