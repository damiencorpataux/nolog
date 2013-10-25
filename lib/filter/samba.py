#!/usb/bin/python

import re
import time
from datetime import datetime

# Example line:
# [2013/04/08 19:12:20.777561,  0] param/loadparm.c:9114(process_usershare_file)
#   process_usershare_file: stat of /var/lib/samba/usershares/admin$ failed. No such file or directory
re_line = re.compile('^\[(?P<time>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d+)\,\s*\d+\] (?P<message>.*)', re.M|re.DOTALL) #$

def filter(lines):
    data = []
    for line in lines:
        line = '\n'.join([l.strip() for l in line.splitlines()])
        print 'Matching line: %s' % line
        m = re_line.search(line).groupdict()
        m['timestamp'] = time.mktime(time.strptime(m.get('time'), '%Y/%m/%d %H:%M:%S.%f'))
        data.append(m)
    return data
