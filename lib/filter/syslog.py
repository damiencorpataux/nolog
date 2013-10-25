#!/usb/bin/python

import re
import time
from datetime import datetime

# Example line:
# Oct 25 07:03:28 localhost nullmailer[2319]: Sending failed:  Host not found
regex = re.compile('(?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d) (?P<host>.*?) (?P<rawprocess>(?P<process>.\w+)(\[\d+\])?): (?P<message>.*)')

def filter(data):
    for line in data:
        m = regex.search(line).groupdict()
        # FIXME: Timezone
        # TODO: Dates should be parsed in a factorized way
        m['timestamp'] = time.mktime(time.strptime(
            # tweaking non-existing year with current year
            '%s %s' % (datetime.now().year, m.get('time')),
            '%Y %b %d %H:%M:%S'
        ))
        print 'Matched: %s' % m
        yield m
