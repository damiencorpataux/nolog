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
    # Input
    print '\n-- Input:%s --' % plan['input']['input']
    raw = input(plan['input']['input'], plan['input'].get('plan', {}))
    print raw
    # Filter
    print '\n-- Filter:%s --' % plan['filter']['filter']
    processed = filter(plan['filter']['filter'], raw, plan['filter'].get('plan', {}))
    print len(processed), processed
    # Output
    print '\n-- Output:%s --' % plan['output']['output']
    result = output(plan['output']['output'], processed, plan['output'].get('plan', {}))
    print len(result), result

if __name__ == '__main__':
    plan = {
        'input1': {
            'input': 'sshsince',
            'plan': {
                'file': '/var/log/auth.log',
                'user': 'damien',
                'host': 'pistore.local',
                'pre': 'sudo'
            }
        },
        'input': {
            'input': 'grok',
            'plan': {
                'execute': 'echo Hello world'
            }
        },
        'filter': {
            'filter': 'authlog',
        },
        'output': {
            'output': 'mongo',
            'plan': {
                'db': 'test',
                'collection': 'data'
            }
        }
    }
    execute(plan)
