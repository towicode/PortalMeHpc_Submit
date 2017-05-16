#!/usr/bin/env python

# import modules used here -- sys is a very standard one
import sys
import argparse
import logging

import sys
import paramiko
import time

# Gather our code in a main() function


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    print "Hello there."
    k = paramiko.RSAKey.from_private_key_file(args.pkey)
    hostname = args.hostname
    username = args.user
    port = 22
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, port=port, username=username, pkey=k)

        chan = client.invoke_shell()

        buff = ""
        resp = chan.recv(9999)
        buff += resp
        chan.send("ocelote\n")

        while ("from gatekeeper.hpc.arizona.edu") not in buff:
            resp = chan.recv(9999)
            buff += resp
            time.sleep(.001)

        print buff

        pub_file = "test test test"
        chan.send("echo \"" + pub_file + "\" > mypubfile.pub\n")
        time.sleep(1)

        # submit file to queue here.

    finally:
        client.close()


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

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
