#!/usr/bin/python

""" This input does ... """
""" You might want to add this host .ssh/trusted_hosts """
""" and allow sudo without password to $user on $host """

import shell

def process(data, file, host='root@localhost', port='22', pre=''):
    """ Uses since to retrive last line of a remote file """
    """ Warning this can be harmful as the ssh command is excuted as is: """
    """ You might want to create a dedicated user for reading logs """
    files = file if isinstance(file, list) else [file]
    # FIXME: Should return stdout, and log stderr
    #        use paramiko.SSHClient(): http://stackoverflow.com/a/3586168
    cmd = 'ssh -p %s %s "%s"' % (port, host, '; '.join(['%s since %s'%(pre,file) for file in files]))
    return shell.process(data=None, command=cmd)
