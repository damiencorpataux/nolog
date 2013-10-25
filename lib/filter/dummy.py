#!/usb/bin/python

def filter(data):
    for line in data: yield {'raw': line}
