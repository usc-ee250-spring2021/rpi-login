#!/bin/python3

import os,sys,datetime,time,signal
#successlogfile = 'README.md'

#https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

intro=f"""
{bcolors.BOLD}
	__________________________________________________
	EE250 - Distributed Systems and Internet Of Things
	``````````````````````````````````````````````````

{bcolors.WARNING+bcolors.UNDERLINE}
	WARNING! RPi Playground must be used with caution.

{bcolors.HEADER}
	General Information:
{bcolors.ENDC+bcolors.BOLD+bcolors.HEADER}
	1. Try not to shutdown or reboot this RPi
	2. Try not to add packages to the RPi without permission
	3. Report any unusual incidents to the EE250 Staffs
	4. Your logins to this RPi are timestamped and recorded.

"""

outro=f"""
{bcolors.WARNING+bcolors.BOLD}
	__________________________________
	THANK YOU AND HAPPY LEARNING EE250
	``````````````````````````````````
"""

failedloginmsg=f"""
{bcolors.WARNING+bcolors.BOLD} Login Failed! This event has been recored.
"""

def logEvent(text,logfile='',raw=False):
    logtime = datetime.datetime.utcnow().isoformat().split('.')[0]
    PI_USER = os.environ['USER']

    if logfile=='':
        logfile = f'{PI_USER}.md'

    with open(logfile,'a+') as g:
        if raw:
            g.write(text)
        else:
            g.write(f'\n- {logtime} | {PI_USER} -> {text}')

def login():
    logEvent('\n',raw=True) # add an extra newline

    os.system('git pull') #needed synchronise between login of diff users
    
    print(f'{bcolors.BOLD+bcolors.OKBLUE}We use Github [using `git push (--dry-run?)`] for login and USC Email for recording login events')
    while True:
        print(f"{bcolors.WARNING+bcolors.BOLD}Email (@usc.edu): ",end=f'{bcolors.ENDC}')
        uscemail = input().strip()
        if uscemail=='' or (not uscemail.endswith('@usc.edu')):
            continue

        else: break 
    
    logEvent(uscemail) #log

    os.system('git add *.md')
    os.system('git commit -m "{logtext}"')
    cmdstatus = os.system('git push')
    
    if(cmdstatus==0):
        logEvent(f'{uscemail} login succeeded')
        print(intro)
        os.system('cd ~ && bash')
        print(outro)
        time.sleep(3)
        sys.exit(0)
    else:
        logEvent('github login failed')
        print(failedloginmsg)
        time.sleep(3)
        sys.exit(-1)

def signal_handler(sig, frame):
    logtime = datetime.datetime.utcnow().isoformat()
    logEvent(f"SIGINT")
    print(f"\n\n{bcolors.WARNING+bcolors.BOLD}INTERRUPT -> This event has been logged.")
    time.sleep(3)
    sys.exit(-2)


#change to current dir
thisfile = os.path.realpath(__file__)
thisdir = os.path.dirname(thisfile)
os.chdir(thisdir)

#register signal interrupt handler
signal.signal(signal.SIGINT, signal_handler)

#attempt login
login()

#exit
sys.exit(-3) #shouldn't reach here, must be captured by SIGINT


