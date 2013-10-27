#!/usb/bin/python

""" This filter parses /var/log/dpkg.log (debian) """

import re
import time
from datetime import datetime

# Example line:
# 2013-10-27 11:50:48 status half-configured snmp-mibs-downloader:all 1.1
regex = re.compile('(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<command>.*?) (?P<package>.*)')

def process(data):
    for line in data:
        m = regex.search(line).groupdict()
        # FIXME: Timezone
        # TODO: Dates should be parsed in a factorized way
        m['timestamp'] = time.mktime(time.strptime(
            m.get('time'), '%Y-%m-%d %H:%M:%S'
        ))
        yield m
