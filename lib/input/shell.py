#!/usr/bin/python

""" This input does ... """
""" You might want to add this host .ssh/trusted_hosts """
""" and allow sudo without password to $user on $host """

import subprocess

def input(command):
    """ Executes a shell command and returns stdout """
    print 'Command: %s' % command
    #return subprocess.check_output(command, shell=True)
    # FIXME: stderr must be printed (and thus be loggedI)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        print 'Read: %s' % line
        yield line
