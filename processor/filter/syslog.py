#!/usb/bin/python

import re
import time
from datetime import datetime

# Example line:
# Oct 25 07:03:28 localhost nullmailer[2319]: Sending failed:  Host not found
regex = re.compile('(?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d) (?P<host>.*?) (?P<rawprocess>(?P<process>.+?)(\[\d+\])?): (?P<message>.*)')

def process(data, year=None):
    for line in data:
        m = regex.search(line).groupdict()
        # FIXME: Timezone
        # TODO: Dates should be parsed in a factorized way
        year = year if year else datetime.now().year
        m['timestamp'] = time.mktime(time.strptime(
            '%s %s' % (year, m.get('time')), # add current year to logline
            '%Y %b %d %H:%M:%S'
        ))
        yield m
