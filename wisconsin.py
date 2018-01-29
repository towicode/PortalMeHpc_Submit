""" Module for the wisconsin plugin """

import logging
import time
import generics as g


def plugin_main(args, **kwargs):
    """ Modules for submitting to wisconsin """

    logging.debug("Loaded wisconsin module...")

    #   Create connection to jetstream
    child = g.create_shell_and_connect_generic(args)

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
    g.upload_files(child,args, expected)
    g.create_and_submit_generic(child, args, expected)

    logging.info("Wisconsin Completed")
