##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 2/29/2016
##Program Name  : pyTimer
##Description   : Timer python functions to be used with any python code
##Python Version: 2.7.10
##Prereqs Knowledge: Python
##Prereqs Hardware: Any computer
##Prereqs Software: Python, pip
##Python Libraries: time
##Static variables: 
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       02/29/2016    Justin Suelflow      Function creation for timer
##    2       03/31/2016    Justin Suelflow      Added Runtime log
##   2.1      04/11/2016    Justin Suelflow      Changed log file path
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
from datetime import datetime
import time
##*********************END IMPORT*********************##

##*********************FUNCTIONS*********************##
##  Function: startTimer
##  Description: Start timer
##  Parameters: 
##  Returns: float
def startTimer():
    start = time.time()
    return start

##  Function: endTimer
##  Description: End timer and return the time in seconds
##  Parameters: st = float type
##  Returns: string
def endTimer(st, pName):
    end = time.time()
    tot = end - st
##  Format the total time to a floating number with 2 decimal places
    tot = ("{0:.1f}".format(round(tot,2)))
    endStr = str(tot) + " seconds"
    cDate = datetime.now()
    cDate = cDate.strftime('%m/%d/%Y')
    writeRuntimeLog("Program: " + pName + " took " + endStr + " on: " + cDate + "\n")
    return endStr

##  Function	: writeRuntimeLog
##  Description	: Write text to log
##  Parameters	: text = string type
##  Returns	:
def writeRuntimeLog(text):
##  Open a log file and append to the end of the log
    logFile = open('/var/www/html/Logs/pylog_Runtimes.txt','a')
    logFile.write(text)
##  Close log file
    logFile.close()
##*********************END FUNCTIONS*********************##
