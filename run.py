#!/usr/bin/python

# FIXME: Logfile name must be saved with logline hash
#        Input/filters/output names/config and filter process timestamp should be saved
#        Stdout should be logged (eg. enything print'ed)

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
    lines = data if isinstance(data, list) else data.strip().splitlines()
    return filter.filter(lines, **options)
    # FIXME: Oneliner is nice but but parses all, or nothing if there is an error
    #return [r.search(line).groupdict() for line in lines]

def output(output, data=[], options={}):
    # import lib.output.{output} as output
    output = getattr(__import__('lib.output', globals(), locals(), [output], -1), output)
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
    # Filter(s)
    filters = plan['filter'] if isinstance(plan['filter'], list) else [plan['filter']]
    processed = raw
    for f in filters:
        module = f['module'] 
        print '\n-- Filter:%s --' % module
        processed = filter(module, processed, f.get('plan', {}))
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
                'host': 'damien@pistore.local',
                'pre': 'sudo'
            }
        },
        'filter': {
            'module': 'syslog'
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
            'module': 'shell',
            'plan': {
                'command': 'ssh damien@pistore.local sudo find /var/log/samba/ -iname log* -exec "since {} \;"'
            }
        },
        'filter': [{
            'module': 'stacklines',
            'size': 2
        }, {
            'module': 'samba'
        }],
        'output': {
            'module': 'mongo',
            'plan': {
                'db': 'test',
                'collection': 'data'
            }
        }
    }]
    plans.reverse()
    run(plans[0:])
