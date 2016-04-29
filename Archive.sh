#!/bin/bash

fCH="/Scrapes/`date +\%m\%d\%Y`_TorontoStar_Scrape.csv"
fCBC="/Scrapes/`date +\%m\%d\%Y`_TorontoSun_Scrape.csv"
fCTV="/Scrapes/`date +\%m\%d\%Y`_VancouverSun_Scrape.csv"

if [ -f $fCH ] && [ -s $fCH ]; then
	sudo mv $fCH /Scrapes/Archive/
fi

if [ -f $fCBC ] && [ -s $fCBC ]; then
	sudo mv $fCBC /Scrapes/Archive/
fi

if [ -f $fCTV ] && [ -s $fCTV ]; then
	sudo mv $fCTV /Scrapes/Archive/
fi