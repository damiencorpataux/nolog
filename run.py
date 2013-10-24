import subprocess
import re

def shebang(file):
    with open(file, 'r') as f:
        spling = f.readline()
        if spling[0:2] != '#!': raise Exception('No shebang')
        return spling.strip()

# FIXME: Remove this
#        Legacy of a trial to use shell scripts as input
def input_shell(file, args=[]):
    return subprocess.check_output(file)
    # TODO: Yield it
    #popen = subprocess.Popen([file], stdout=subprocess.PIPE)
    #for line in iter(popen.stdout.readline, ""):
    #    yield line

def input(input, options={}):
    input = getattr(__import__('lib.input', globals(), locals(), [input], -1), input)
    return input.input(**options)

# FIXME: Use grok as much as possible
def filter(filter, data=''):
    # import lib.filter.{filter} as filter
    # http://docs.python.org/2/library/functions.html#__import__
    filter = getattr(__import__('lib.filter', globals(), locals(), [filter], -1), filter)
    lines = data.strip().split('\n')
    processed = []
    try:
        for line in lines: processed.append(filter.filter(line))
    except Exception:
        print('Error: parsing log line')
        pass
    return processed
    # FIXME: Oneliner is nice but but parses all,
    #        or nothing if there is an error
    #return [r.search(line).groupdict() for line in lines]

def output(output, data=[]):
    # import lib.filter.{output} as output
    # http://docs.python.org/2/library/functions.html#__import__
    output = getattr(__import__('lib.output', globals(), locals(), [output], -1), output)
    output.output(data)

def execute():
    # TODO: Yield data, really
    raw = input('sshsince', {
        'file': '/var/log/auth.log',
        'user': 'damien',
        'host': 'pistore.local',
        'pre': 'sudo'
    })
    print(raw)
    processed = filter('authlog', raw)
    print(processed, len(processed))
    output('mongo', processed)

execute()
