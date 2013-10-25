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
    #lines = data if isinstance(data, list) else data.strip().splitlines()
    yield filter.filter(data, **options)
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
    input_data = input(module, plan['input'].get('plan', {}))
    print input_data
    # Filter(s)
    filters = plan['filter'] if isinstance(plan['filter'], list) else [plan['filter']]
    filter_data = input_data
    for f in filters:
        module = f['module'] 
        print '\n-- Filter:%s --' % module
        filter_data = filter(module, filter_data, f.get('plan', {}))
        print filter_data
    # Output
    module = plan['output']['module'] 
    print '\n-- Output:%s --' % module
    inserts = output(module, filter_data, plan['output'].get('plan', {}))
    for insert in inserts: print insert

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
                'collection': 'data2'
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
            'module': 'dummy',#'stacklines',
            'count': 2
        #}, {
        #    'module': 'samba'
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
    run(plans[0:1])
