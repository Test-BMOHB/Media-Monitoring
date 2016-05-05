#!/bin/bash
##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 5/4/2016
##Program Name  : scrapes.sh
##Description   : Runs the python scrape files
##Prereqs Knowledge: Unix Bash scripting
##Prereqs Hardware: Unix VM
##Prereqs Software:
##Run command: sudo bash scrapes.sh
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       05/04/2016    Justin Suelflow    Initial Version
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##
# Run python scrapes and save output to the Log files
# 2>&1 means to move the standard output and error output of the scrapes to the logs
# ; means that the next line is dependent on the current line completing regardless of failure or success
sudo python /Code/pyScrape_CalgaryHerald.py >> /Logs/pylog_CalgaryHerald.txt 2>&1 ;
sudo python /Code/pyScrape_CBCNews.py >> /Logs/pylog_CBCNews.txt 2>&1 ;
sudo python /Code/pyScrape_CTVNews.py >> /Logs/pylog_CTVNews.txt 2>&1