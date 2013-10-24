import subprocess
import re

def input(file, args=[]):
    # Unuseful for now, we might check of the interpreter in the future
    with open(file, 'r') as f: shebang = f.readline()
    print shebang
    #
    return subprocess.check_output(file)
    # TODO: Yield it
    #popen = subprocess.Popen([file], stdout=subprocess.PIPE)
    #for line in iter(popen.stdout.readline, ""):
    #    yield line

def filter(file, data=[]):
    lines = data.strip().split('\n')[0:5]
    # named regex are useful
    r = re.compile('^(?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d)\s(?P<data>.*)$')
    return [r.search(line).groupdict() for line in lines]

def output(file, data=[]):
    return data

def execute(file):
    # TODO: Data has to be yield really
    raw = input(file)
    print raw
    processed = filter(None, raw)
    print processed, len(processed)
    output(None, processed)

execute('lib/input/ssh-since')
