#!/usb/bin/python

import subprocess

def process(data=None, execute='cat -', pattern='.*', reaction='%{@LINE}'):
    file = '/tmp/nolog.grok'
    program = ' \
        program { \
          exec "%s" \
          match { \
            pattern: "%s" \
            reaction: "%s" \
          } \
        } \
    ' % (execute, pattern, reaction)
    with open(file, 'w+') as f:
        f.seek(0)
        f.write(program)
    return subprocess.check_output(['grok', '-f', file], stderr=subprocess.STDOUT)
