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
## Version  | ddmmyyyy  |  User           |                Changes
##    1       29022016    Justin Suelflow      Function creation for timer
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
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
def endTimer(st):
    end = time.time()
    tot = end - st
##  Format the total time to a floating number with 2 decimal places
    tot = ("{0:.1f}".format(round(tot,2)))
    endStr = str(tot) + " seconds"
    return endStr
##*********************END FUNCTIONS*********************##
