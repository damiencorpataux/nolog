#!/usb/bin/python

def process(data):
    for line in data: yield {'raw': line}
