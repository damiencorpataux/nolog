#!/usb/bin/python

import re
import time
from datetime import datetime

# named regex are useful
re_line = re.compile('^(?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d) (?P<host>.*?) (?P<rawprocess>(?P<process>.\w+)(\[\d+\])?): (?P<message>.*)$')

def filter(lines):
    data = []
    for line in lines:
        m = re_line.search(line).groupdict()
        # Extracts date, format: Oct 24 19:03:02
        # FIXME: Timezone
        # TODO: Dates should be parsed in a factorized way
        m['timestamp'] = time.mktime(time.strptime(
            # tweaking non-existing year with current year
            '%s %s' % (datetime.now().year, m.get('time')),
            '%Y %b %d %H:%M:%S'
        ))
        data.append(m)
    return data
