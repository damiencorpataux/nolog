#!/usr/bin/python

# FIXME: - Timezone should be managed using a factorized component
#        - A filter should add necessary information to data
#          (e.g. log filename, process timestamp and source hostname, processing timestamp, input/filters/outputs names and configs)
#        - Stdout should be logged (eg. enything print'ed)
#        - in execute(), rename the 'actions' variable to module, and 'module' attr to 'name', and
#          in conf/sample.py, rename the 'module' attr to 'name'
#          because this engine pipes modules



def execute(plan):
    print '\n-- Plan:'
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
    count = 0
    for result in data:
        count += 1
        print 'Done: %s' % result
    print '- %s items.' % count

def run(plans):
    for plan in plans:
        execute(plan)
    print '\nPlan executed.'

if __name__ == '__main__':
    from conf.sample import plan
    run(plan)
