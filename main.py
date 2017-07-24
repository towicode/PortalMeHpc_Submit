#!/usr/bin/env python

# import modules used here -- sys is a very standard one
import sys
import argparse
import logging

import sys
import pexpect
import time

import os

# Gather our code in a main() function


def submit_uofa(args):
    

    pexpect.spawn("ssh-keyscan hpc.arizona.edu >> ~/.ssh/known_hosts")
    time.sleep(5)

    os.chmod(str(args.pkey), 0600)
    child = pexpect.spawn("ssh -i" +str(args.pkey)+ " " + str(args.user) +
                              "@" + str(args.hostname) + "")

    index = child.expect(['Are you sure you want to continue connecting*',
                          pexpect.EOF, pexpect.TIMEOUT], timeout=5)
    logging.debug(child.before)
    if index == 0:
        child.sendline("yes")
        time.sleep(5)

    child.expect("Shortcut commands to access*")
    logging.debug(child.before)



    child.sendline("touch .portalme")
    time.sleep(5)
    child.expect("~]\$")
    logging.debug(child.before)
    time.sleep(5)


    time.sleep(5)
    child.sendline(args.resource)
    child.expect("from gatekeeper.hpc.arizona.edu*")
    logging.debug(child.before)


    child.sendline("rm mysubmit.file")
    time.sleep(5)
    child.expect("~]\$")
    logging.debug(child.before)
    time.sleep(5)



    #   Create script file from input file.
    with open(args.script, 'r') as myfile:
        for line in myfile:
            line = line.replace('\r', '').replace('\n', '').replace('\\','\\\\').replace('$', '\$').replace('"', '\\\"')
            logging.debug(line)
            child.sendline("echo \"" + line + "\" >> mysubmit.file")
            child.expect("~]\$")

        # submit file to queue here.
        child.sendline(args.submit + " mysubmit.file")
        child.expect("~]\$")
        logging.debug(child.before)

        child.expect("~]\$")
        logging.debug(child.before)
    
    logging.info("Completed")


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    submit_uofa(args)



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
        "-S",
        "--submit",
        help="command to submit, ex qsub.",
        nargs="?",
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
        "-G",
        "--gatekeepers",
        help="Useful for HPC with gatekeepers, see docs for more info",
        nargs="?",
        default="",
        type=str)
    

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
