#!/usb/bin/python

import re

# named regex are useful
regex = re.compile('^(?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d)\s(?P<data>.*)$')

def filter(line):
    return regex.search(line).groupdict()
