#!/usr/bin/env python
import sys
import argparse
import logging
import sys
import pexpect
import time
import os

# Gather our code in a main() function


def submit_jetstream(args):
    """ Modules for submitting to Jetstream """

    logging.debug("Loaded Jetstream module...")

    #   Create connection to jetstream
    child = create_shell_and_connect_generic(args)

    #   Set expected as part of terminal response. In this case jetstream is 'towicode@f2....:~""
    expected = args.user+"@"

    #   Wait for prompt to be active
    child.expect(expected)

    #   Remove old submit file
    child.sendline("rm mysubmit.file")
    time.sleep(2)
    
    #   Wait for prompt to be active.
    child.expect(expected)
    logging.debug(child.before)
    time.sleep(2)

    #   Create the file and submit!
    create_and_submit_generic(child, args, expected)

    logging.info("Completed")

def create_shell_and_connect_generic(args):
    """Creates a shell, makes sure the key is the right permission and then 
    attempts to connect, rerturns shell instance """


    pexpect.spawn("ssh-keyscan "+args.hostname+" >> ~/.ssh/known_hosts")
    time.sleep(5)

    os.chmod(str(args.pkey), 0600)

    logging.debug("Starting SSH Instance... this may take a minute.")
    child = pexpect.spawn("ssh -i" +str(args.pkey)+ " " + str(args.user) +
                              "@" + str(args.hostname) + "")

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

        # submit file to queue here.
        if (args.submit):
            child.sendline(args.submit + " mysubmit.file")
        else:
            child.sendline("chmod +x mysubmit.file")
            child.sendline("./"+ "mysubmit.file")

        child.expect(expected)
        logging.debug(child.before)

        child.expect(expected)
        logging.debug(child.before)



def submit_uofa(args):
    """ Code specifically for submitting to the UOFA 

    Can be used as a template for other modules """

    logging.debug("Loaded UOFA module...")
    
    #   Create instance of shell
    child = create_shell_and_connect_generic(args)

    #   Finally we should be at the window where you can access the different HPCS (ocelote, etc)
    child.expect("Shortcut commands to access*")
    logging.debug(child.before)

    expected = "~]\$"

    #   Create basic ('ive been here') file for testing.
    child.sendline("touch .portalme")
    time.sleep(5)
    child.expect(expected)
    logging.debug(child.before)
    time.sleep(5)


    #   Attempt to login to resource ('ocelote')
    time.sleep(5)
    child.sendline(args.resource)
    child.expect("from gatekeeper.hpc.arizona.edu*")
    logging.debug(child.before)

    #   remove all previous files.
    child.sendline("rm mysubmit.file")
    time.sleep(5)
    child.expect(expected)
    logging.debug(child.before)
    time.sleep(5)

    #   Create a submit script
    create_and_submit_generic(child, args, expected)
        
    logging.info("Completed")


def main(args, loglevel):
    """ Entry point after we gather arguments from the command line 

    We load the function by name, prepended with submit_.
    Additionally logging is setup here. """

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    current_module = sys.modules[__name__]
    method = getattr(current_module, "submit_"+args.module, default_action)

    logging.debug("Starting...")
    method(args)

def default_action(args):
    """ Basic default action if the user provides a module that doesn't exist """

    logging.error("We couldn't find the correct module! Note that submit_ is prepended to your 'def' name")
    exit(1)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates a PBS submit script on HPC and executes it.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        "-u",
        "--user",
        help="User to be passed to ssh 'user@host...'",
        nargs="?",
        required=True,
        type=str)
    required.add_argument(
        "-P",
        "--pkey",
        help="Private key to be used to connect to SSH",
        nargs="?",
        required=True,
        type=str)

    required.add_argument(
        "-s",
        "--script",
        help="Script that will be remotely executed",
        nargs="?",
        required=True,
        type=str)



    required.add_argument(
        "-M",
        "--module",
        help="The module (or system) you would like to use. Default UOFA HPC",
        nargs="?",
        default="uofa",
        required=True,
        type=str)

    optional = parser.add_argument_group('optional arguments')

    optional.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")

    optional.add_argument(
        "-p",
        "--port",
        help="port to be used to connect",
        nargs="?",
        default="22",
        type=str)

    optional.add_argument(
        "-H",
        "--hostname",
        help="host for ssh. 'user@host...'",
        nargs="?",
        default="hpc.arizona.edu",
        type=str)

    optional.add_argument(
        "-r",
        "--resource",
        help="Which resource would you like to execute on (UofA only, default: ocelote)",
        nargs="?",
        default="ocelote",
        type=str)

    optional.add_argument(
        "--key",
        help="Two Factor Key",
        nargs="?",
        default="ocelote",
        type=str)

    optional.add_argument(
        "-S",
        "--submit",
        help="command to submit, ex qsub. default './' as in executed.",
        nargs="?",
        required=False,
        type=str)

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
