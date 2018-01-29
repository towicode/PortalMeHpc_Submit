#!/usr/bin/env python
import sys
import argparse
import logging
import sys
import pexpect
import time
import os
import generics as g

# Gather our code in a main() function


def load_plugin(name):
    mod = __import__("%s" % name)
    return mod

def call_plugin(name, *args, **kwargs):
    plugin = load_plugin(name)
    plugin.plugin_main(*args, **kwargs)


def main(args, loglevel):
    """ Entry point after we gather arguments from the command line 

    We load the function by name, prepended with submit_.
    Additionally logging is setup here. """

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    #   current_module = sys.modules[__name__]
    #   method = getattr(current_module, "submit_"+args.module, default_action)

    logging.debug("Starting...")
    #   method(args)

    call_plugin(args.module, args)


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
