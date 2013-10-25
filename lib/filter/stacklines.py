#!/usb/bin/python

def filter(lines, size=2):
    return ['\n'.join(lines[n:n+size]) for n in range(0, len(lines), size)]
