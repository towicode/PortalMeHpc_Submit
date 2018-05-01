import sys
import argparse
import logging
import sys
import pexpect
import time
import os



def create_shell_and_connect_generic(args):
    """Creates a shell, makes sure the key is the right permission and then 
    attempts to connect, rerturns shell instance """


    pexpect.spawn("ssh-keyscan "+args.hostname+" >> ~/.ssh/known_hosts")
    time.sleep(5)

    os.chmod(str(args.pkey), 0600)

    logging.debug("Starting SSH Instance... this may take a minute.")
    child = pexpect.spawn("ssh -i" +str(args.pkey)+ " " + str(args.user) +
                              "@" + str(args.hostname) + " -p " + str(args.port))

    #   There is a chance on first time to display this message. we need to handle it.
    index = child.expect(['Are you sure you want to continue connecting*',
                          pexpect.EOF, pexpect.TIMEOUT], timeout=5)
    logging.debug(child.before)

    #   If the index == 0, that means the message was present.
    if index == 0:
        child.sendline("yes")
        time.sleep(2)

    return child

def create_and_submit_generic(child, args, expected):
    """Creates and submits the file with the the open ssh instance"""

    with open(args.script, 'r') as myfile:
        for line in myfile:
            line = line.replace('\r', '').replace('\n', '').replace('\\','\\\\').replace('$', '\$').replace('"', '\\\"')
            logging.debug(line)
            child.sendline("echo \"" + line + "\" >> mysubmit.file")
            child.expect(expected)

        time.sleep(2)

        # submit file to queue here.
        if (args.submit):
            child.sendline(args.submit + " mysubmit.file")
        else:
            child.sendline("chmod +x mysubmit.file")
            child.sendline("nohup ./mysubmit.file &")

        time.sleep(1)

        child.expect(expected)
        logging.debug(child.before)

        child.expect(expected)
        logging.debug(child.before)

def upload_files(child, args, expected):
    """creates files added to args"""
    for f in args.files:
        name = os.path.basename(f.name)
        #   move old file
        child.sendline("mv " + name + " " + name + "_old" + str(os.getpid()))
        child.expect(expected)
        #   write new file
        for line in f:
            line = line.replace('\r', '').replace('\n', '').replace('\\','\\\\').replace('$', '\$').replace('"', '\\\"')
            logging.debug(line)
            child.sendline("echo \"" + line + "\" >> " + name)
            logging.debug("attempted to send atleast")
            child.expect(expected)
        time.sleep(2)