#!/usb/bin/python

def filter(line):
    return {
        'time': '1970-01-01 00:00:00.000+0000',
        'data': line
    }
