#!/usr/bin/python

# FIXME: Logfile name must be saved with logline hash
#        Input/filters/output names/config and filter process timestamp should be saved
#        Stdout should be logged (eg. enything print'ed)

def shebang(file):
    with open(file, 'r') as f:
        spling = f.readline()
        if spling[0:2] != '#!': raise Exception('No shebang')
        return spling.strip()

def input(input, data=None, options={}):
    # import lib.input.{input} as input
    # http://docs.python.org/2/library/functions.html#__import__
    input = getattr(__import__('lib.input', globals(), locals(), [input], -1), input)
    return input.input(**options)

# FIXME: Use grok as much as possible
def filter(filter, data=None, options={}):
    # import lib.filter.{filter} as filter
    print filter
    filter = getattr(__import__('lib.filter', globals(), locals(), [filter], -1), filter)
    #lines = data if isinstance(data, list) else data.strip().splitlines()
    return filter.filter(data, **options)
    # FIXME: Oneliner is nice but but parses all, or nothing if there is an error
    #return [r.search(line).groupdict() for line in lines]

def output(output, data=[], options={}):
    # import lib.output.{output} as output
    output = getattr(__import__('lib.output', globals(), locals(), [output], -1), output)
    return output.output(data, **options)

def execute(plan):
    # Executes input/filter/output steps
    data = None
    for step in [input, filter, output]:
        actions = plan[step.func_name] if isinstance(plan[step.func_name], list) else [plan[step.func_name]]
        for action in actions:
            module = action.get('module')
            options = action.get('options', {})
            print '- %s: %s, %s' % (step.__name__, module, options)
            data = step(module, data=data, options=options)
    # Results
    print '\n-- Excution:'
    for result in data:
        print 'Done: %s' % result
        print

def run(plans):
    for plan in plans:
        execute(plan)
    print 'Plan executed.'

if __name__ == '__main__':
    plans = [{
        'input': {
            'module': 'sshsince',
            'options': {
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
            'options': {
                'db': 'test',
                'collection': 'data2'
            }
        }
    }, {
        'input': {
            'module': 'shell',
            'options': {
                'command': 'ssh damien@pistore.local sudo find /var/log/samba/ -iname log* -exec "since {} \;"'
            }
        },
        'filter': [{
            'module': 'dummy',#'stacklines',
            'count': 2
        }, {
            'module': 'samba'
        }],
        'output': {
            'module': 'mongo',
            'options': {
                'db': 'test',
                'collection': 'data'
            }
        }
    }, {
        'input': {
            'module': 'shell', 'options': {'command': 'ssh damien@pistore.local sudo tail /var/log/samba/log.smbd'}
            #'module': 'sshsince', 'options': {
            #    'file': '/var/log/samba/smb.log',
            #    'host': 'damien@pistore.local',
            #    'pre': 'sudo'
            #}
        },
        'filter': [{
            'module': 'stacklines', 'options': {'count':2}
        }, {
            'module': 'samba',
        }],
        'output': {
            'module': 'mongo'
        }
    }]
    #plans.reverse()
    run(plans)
