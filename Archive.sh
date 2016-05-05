#!/bin/bash
##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 5/4/2016
##Program Name  : Archive.sh
##Description   : Archives the files if they have data
##Prereqs Knowledge: Unix Bash scripting
##Prereqs Hardware: Unix VM
##Prereqs Software:
##Run command: sudo bash Archive.sh
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       05/04/2016    Justin Suelflow    Initial Version
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##
# Create file variables for where they are located on the VM
fCH="/Scrapes/`date +\%m\%d\%Y`_CalgaryHerald_Scrape.csv"
fCBC="/Scrapes/`date +\%m\%d\%Y`_CBCNews_Scrape.csv"
fCTV="/Scrapes/`date +\%m\%d\%Y`_CTVNews_Scrape.csv"
# If files exist (-f) and are not empty (-s), then move the files to the Archive folder
if [ -f $fCH ] && [ -s $fCH ]; then
	sudo mv $fCH /Scrapes/Archive/
fi

if [ -f $fCBC ] && [ -s $fCBC ]; then
	sudo mv $fCBC /Scrapes/Archive/
fi

if [ -f $fCTV ] && [ -s $fCTV ]; then
	sudo mv $fCTV /Scrapes/Archive/
fi