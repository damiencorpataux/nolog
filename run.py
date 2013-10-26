#!/usr/bin/python

# FIXME: Logfile name must be saved with logline hash
#        Input/filters/output names/config and filter process timestamp should be saved
#        Stdout should be logged (eg. enything print'ed)

def shebang(file):
    with open(file, 'r') as f:
        spling = f.readline()
        if spling[0:2] != '#!': raise Exception('No shebang')
        return spling.strip()

def execute(plan):
    # Executes input/filter/output steps
    data = None
    for step in ['input', 'filter', 'output']:
        actions = plan[step] if isinstance(plan[step], list) else [plan[step]]
        for action in actions:
            module = action.get('module')
            options = action.get('options', {})
            print '- %s: %s, %s' % (step, module, options)
            # import processor.{step}.{module} as {m}
            # http://docs.python.org/2/library/functions.html#__import__
            m = getattr(__import__('.'.join(['processor', step]), globals(), locals(), [module], -1), module)
            data = m.process(data=data, **options)
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
