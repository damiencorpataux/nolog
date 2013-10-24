#!/usr/bin/python

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
    lines = data.strip().split('\n')
    processed = []
    try:
        for line in lines: processed.append(filter.filter(line, **options))
    except Exception:
        # TODO: Log the failed line and the raised exception
        print('Error: parsing log line')
        pass
    return processed
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

if __name__ == '__main__':
    plan = {
        'input1': {
            'module': 'sshsince',
            'plan': {
                'file': '/var/log/auth.log',
                'user': 'damien',
                'host': 'pistore.local',
                'pre': 'sudo'
            }
        },
        'input': {
            'module': 'grok',
            'plan': {
                'execute': 'ssh damien@pistore.local sudo since /var/log/auth.log'
            }
        },
        'filter': {
            'module': 'authlog',
        },
        'output': {
            'module': 'mongo',
            'plan': {
                'db': 'test',
                'collection': 'data'
            }
        }
    }
    execute(plan)
