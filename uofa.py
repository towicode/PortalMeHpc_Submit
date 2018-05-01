""" Module for the wisconsin plugin """

import logging
import time
import generics as g


def plugin_main(args, **kwargs):
    """ Code specifically for submitting to the UOFA 
    Can be used as a template for other modules """

    logging.debug("Loaded UOFA module...")
    
    #   Create instance of shell
    child = g.create_shell_and_connect_generic(args)

    #   Finally we should be at the window where you can access the different HPCS (ocelote, etc)
    child.expect("Shortcut commands to access*")
    logging.debug(child.before)

    expected = args.user + "@"

    #   Create basic ('ive been here') file for testing.
    child.sendline("touch .portalme")
    time.sleep(2)
    child.expect(expected)
    logging.debug(child.before)
    time.sleep(2)


    #   Attempt to login to resource ('ocelote')
    time.sleep(2)
    child.sendline(args.resource)
    child.expect(".hpc.arizona.edu*")
    logging.debug(child.before)

    #   remove all previous files.
    child.sendline("rm mysubmit.file")
    time.sleep(2)
    child.expect(expected)
    logging.debug(child.before)
    time.sleep(2)

    #   Create a submit script
    g.create_and_submit_generic(child, args, expected)
        
    logging.info("Completed")

