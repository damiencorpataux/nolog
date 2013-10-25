#!/usr/bin/python

# FIXME: Logfile name must be saved with logline hash
#        Input/filters/output names/config and filter process timestamp should be saved

def shebang(file):
    with open(file, 'r') as f:
        spling = f.readline()
        if spling[0:2] != '#!': raise Exception('No shebang')
        return spling.strip()

def input(input, options={}):
    # import lib.input.{input} as input
    # http://docs.python.org/2/library/functions.html#__import__
    input = getattr(__import__('lib.input', globals(), locals(), [input], -1), input)
    return input.input(**options)

# FIXME: Use grok as much as possible
def filter(filter, data='', options={}):
    # import lib.filter.{filter} as filter
    filter = getattr(__import__('lib.filter', globals(), locals(), [filter], -1), filter)
    if not isinstance(data, str): raise Exception('Filter "%s" must return a string' % filter.__name__)
    lines = data.strip().split('\n')
    return filter.filter(lines, **options)
    # FIXME: Oneliner is nice but but parses all, or nothing if there is an error
    #return [r.search(line).groupdict() for line in lines]

def output(output, data=[], options={}):
    # import lib.output.{output} as output
    output = getattr(__import__('lib.output', globals(), locals(), [output], -1), output)
    if not isinstance(data, list): raise Exception('Filter "%s" must return a list' % filter.__name__)
    return output.output(data, **options)

def execute(plan):
    """ Execute the plan and returns the output, if any """
    # TODO: Yield data, really
    #       Make input/filter/output optional because grok can exec: if plan.get('input'): ...
    print 'Executing plan...'
    # Input
    module = plan['input']['module']
    print '\n-- Input:%s --' % module 
    raw = input(module, plan['input'].get('plan', {}))
    print raw
    # Filter
    module = plan['filter']['module'] 
    print '\n-- Filter:%s --' % module
    processed = filter(plan['filter']['module'], raw, plan['filter'].get('plan', {}))
    print len(processed), processed
    # Output
    module = plan['output']['module'] 
    print '\n-- Output:%s --' % module
    result = output(module, processed, plan['output'].get('plan', {}))
    print len(result), result

def run(plans):
    for plan in plans:
        execute(plan)

if __name__ == '__main__':
    plans = [{
        'input': {
            'module': 'sshsince',
            'plan': {
                'file': ['/var/log/auth.log', '/var/log/syslog', '/var/log/daemon.log', '/var/log/messages'],
                'user': 'damien',
                'host': 'pistore.local',
                'pre': 'sudo'
            }
        },
        'filter': {
            'module': 'syslog',
        },
        'output': {
            'module': 'mongo',
            'plan': {
                'db': 'test',
                'collection': 'data'
            }
        }
    }, {
        'input': {
            'module': 'grok',
            'plan': {
                #'execute': 'ssh damien@pistore.local sudo find /var/log/samba/log* -exec since {} \;'
                'execute': 'ssh damien@pistore.local sudo cat /var/log/samba/log.registratura'
            }
        },
        'filter': {
            'module': 'stacklines',
        },
        'output': {
            'module': 'mongo',
            'plan': {
                'db': 'test',
                'collection': 'data'
            }
        }
    }]
    run(plans[0:1])
