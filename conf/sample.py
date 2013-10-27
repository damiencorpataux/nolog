local_mongo = {
    'module': 'mongo',
    'options': {
        'db': 'test',
        'collection': 'data'
    }
}

plan = [{
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
    'output': local_mongo
}, {
    'input': {
        'module': 'shell',
        'options': { 'command': 'ssh damien@pistore.local sudo find /var/log/samba/ -iname log* -exec "since {} \;"' }
    },
    'filter': [{
        'module': 'stacklines',
        'options': { 'count': 2 }
    }, {
        'module': 'samba'
    }],
    'output': local_mongo
}, {
    'input': {
        'module': 'shell', 'options': {'command': 'sudo since /var/log/syslog; sudo since /var/log/auth.log; sudo since /var/log/daemon.log'}
    },
    'filter': { 'module': 'syslog' },
    'output': [
        local_mongo,
        { 'module': 'stdout' }
    ]
}, {
    'input': {
        'module': 'shell', 'options': {'command': 'sudo cat /var/log/dpkg.log'}
    },
    'filter': { 'module': 'dpkg' },
    'output': [
        local_mongo,
        { 'module': 'stdout' }
    ]
}, {
    'input': {
        'module': 'shell', 'options': {'command': 'sudo cat /var/log/syslog; sudo cat /var/log/auth.log; sudo cat /var/log/daemon.log'}
    },
    'filter': { 'module': 'syslog' },
    'output': [
        local_mongo,
        { 'module': 'stdout' }
    ]
}]
plan = plan
