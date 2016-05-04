#!/bin/bash
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