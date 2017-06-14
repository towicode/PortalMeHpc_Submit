```
usage: main.py [-h] -u [USER] -P [PKEY] -s [SCRIPT] -S [SUBMIT] [-v]
               [-p [PORT]] [-H [HOSTNAME]] [-r [RESOURCE]] [-G 
[GATEKEEPERS]] Creates a PBS submit script on HPC and executes it. 
optional arguments:
  -h, --help show this help message and exit required arguments:
  -u [USER], --user [USER]
                        User to be passed to ssh 'user@host...'
  -P [PKEY], --pkey [PKEY]
                        Private key to be used to connect to SSH
  -s [SCRIPT], --script [SCRIPT]
                        Script that will be remotely executed
  -S [SUBMIT], --submit [SUBMIT]
                        command to submit, ex qsub. optional 
arguments:
  -v, --verbose increase output verbosity
  -p [PORT], --port [PORT]
                        port to be used to connect
  -H [HOSTNAME], --hostname [HOSTNAME]
                        host for ssh. 'user@host...'
  -r [RESOURCE], --resource [RESOURCE]
                        Which resource would you like to execute on 
                        (UofA only, default: ocelote)
  -G [GATEKEEPERS], --gatekeepers [GATEKEEPERS]
                        Useful for HPC with gatekeepers, see docs for 
                        more info 
                        
As an alternative to the commandline, 
params can be placed in a file, one per
line, and specified on the commandline like 'main.py @params.conf'.
```
