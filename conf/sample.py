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
    'output': {
        'module': 'mongo',
        'options': {
            'db': 'test',
            'collection': 'data'
        }
    }
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
    'output': {
        'module': 'mongo',
        'options': {
            'db': 'test',
            'collection': 'data'
        }
    }
}, {
    'input': {
        'module': 'shell', 'options': {'command': 'ssh damien@pistore.local sudo tail -n120 /var/log/samba/log.smbd'}
        #'module': 'sshsince', 'options': {
        #    'file': '/var/log/samba/smb.log',
        #    'host': 'damien@pistore.local',
        #    'pre': 'sudo'
        #}
    },
    'filter': [{
        'module': 'stacklines',
        'options': {'count':2}
    }, {
        'module': 'raw',#'samba',
    }],
    'output': [
        { 'module': 'mongo' },
        { 'module': 'stdout' }
    ]
}]
