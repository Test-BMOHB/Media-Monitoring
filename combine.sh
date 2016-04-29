#!/bin/bash

sudo awk 'FNR==1 && NR!=1{next;}{print}' /var/www/html/*_MMJScrape.csv > /var/www/html/MMJ_Merged.csv &&
sudo mv /var/www/html/MMJ_Merged.csv /var/www/html/`date +\%m\%d\%Y`_MMJ_Merged.csv

fBP="/var/www/html/`date +\%m\%d\%Y`_ScreenScrape.csv"
fWM="/var/www/html/`date +\%m\%d\%Y`_Weedmaps_MMJScrape.csv"
fL="/var/www/html/`date +\%m\%d\%Y`_Leafly_MMJScrape.csv"
fPL="/var/www/html/`date +\%m\%d\%Y`_PotLocator_MMJScrape.csv"
fF="/var/www/html/`date +\%m\%d\%Y`_Fintrac_Scrape.csv"
fCRA="/var/www/html/`date +\%m\%d\%Y`_CRA_Scrape.csv"
fCBSA="/var/www/html/`date +\%m\%d\%Y`_CBSA_Scrape.csv"
fMMJ="/var/www/html/`date +\%m\%d\%Y`_MMJ_Merged.csv"
fGN="/var/www/html/`date +\%m\%d\%Y`_GoogleNews_Scrape.csv"
fMG="/var/www/html/`date +\%m\%d\%Y`_MontrealGazette_Scrape.csv"
fGNP="/var/www/html/`date +\%m\%d\%Y`_GoogleNewsPanama_Scrape.csv"
fNP="/var/www/html/`date +\%m\%d\%Y`_NationalPost_Scrape.csv"
fCH="/var/www/html/`date +\%m\%d\%Y`_CalgaryHerald_Scrape.csv"
fCBC="/var/www/html/`date +\%m\%d\%Y`_CBCNews_Scrape.csv"
fCTV="/var/www/html/`date +\%m\%d\%Y`_CTVNews_Scrape.csv"
fGM="/var/www/html/`date +\%m\%d\%Y`_GlobeMail_Scrape.csv"
fOC="/var/www/html/`date +\%m\%d\%Y`_OttawaCitizen_Scrape.csv"
fTST="/var/www/html/`date +\%m\%d\%Y`_TorontoStar_Scrape.csv"
fTSu="/var/www/html/`date +\%m\%d\%Y`_TorontoSun_Scrape.csv"
fVS="/var/www/html/`date +\%m\%d\%Y`_VancouverSun_Scrape.csv"

if [ -f $fBP ] && [ -s $fBP ]; then
	sudo rm /var/www/html/Current/ScreenScrape.csv &&
	sudo cp $fBP /var/www/html/Current/ &&
	sudo mv $fBP /var/www/html/Archive/
fi

if [ -f $fWM ] && [ -s $fWM ]; then
	sudo rm /var/www/html/Current/Weedmaps_MMJScrape.csv &&
	sudo cp $fWM /var/www/html/Current/ &&
	sudo mv $fWM /var/www/html/Archive/
fi

if [ -f $fL ] && [ -s $fL ]; then
	sudo rm /var/www/html/Current/Leafly_MMJScrape.csv &&
	sudo cp $fL /var/www/html/Current/ &&
	sudo mv $fL /var/www/html/Archive/
fi

if [ -f $fPL ] && [ -s $fPL ]; then
	sudo rm /var/www/html/Current/PotLocator_MMJScrape.csv &&
	sudo cp $fPL /var/www/html/Current/ &&
	sudo mv $fPL /var/www/html/Archive/
fi

if [ -f $fF ] && [ -s $fF ]; then
	sudo rm /var/www/html/Current/Fintrac_Scrape.csv &&
	sudo cp $fF /var/www/html/Current/ &&
	sudo mv $fF /var/www/html/Archive/
fi

if [ -f $fCRA ] && [ -s $fCRA ]; then
	sudo rm /var/www/html/Current/CRA_Scrape.csv &&
	sudo cp $fCRA /var/www/html/Current/ &&
	sudo mv $fCRA /var/www/html/Archive/
fi

if [ -f $fCBSA ] && [ -s $fCBSA ]; then
	sudo rm /var/www/html/Current/CBSA_Scrape.csv &&
	sudo cp $fCBSA /var/www/html/Current/ &&
	sudo mv $fCBSA /var/www/html/Archive/
fi

if [ -f $fMMJ ] && [ -s $fMMJ ]; then
	sudo rm /var/www/html/Current/MMJ_Merged.csv &&
	sudo cp $fMMJ /var/www/html/Current/ &&
	sudo mv $fMMJ /var/www/html/Archive/
fi

if [ -f $fGN ] && [ -s $fGN ]; then
	sudo rm /var/www/html/Current/GoogleNews_Scrape.csv &&
	sudo cp $fGN /var/www/html/Current/ &&
	sudo mv $fGN /var/www/html/Archive/
fi

if [ -f $fMG ] && [ -s $fMG ]; then
	sudo rm /var/www/html/Current/MontrealGazette_Scrape.csv &&
	sudo cp $fMG /var/www/html/Current/ &&
	sudo mv $fMG /var/www/html/Archive/
fi

if [ -f $fGNP ] && [ -s $fGNP ]; then
	sudo rm /var/www/html/Current/GoogleNewsPanama_Scrape.csv &&
	sudo cp $fGNP /var/www/html/Current/ &&
	sudo mv $fGNP /var/www/html/Archive/
fi

if [ -f $fNP ] && [ -s $fNP ]; then
	sudo rm /var/www/html/Current/NationalPost_Scrape.csv &&
	sudo cp $fNP /var/www/html/Current/ &&
	sudo mv $fNP /var/www/html/Archive/
fi

if [ -f $fCH ] && [ -s $fCH ]; then
	sudo rm /var/www/html/Current/CalgaryHerald_Scrape.csv &&
	sudo cp $fCH /var/www/html/Current/ &&
	sudo mv $fCH /var/www/html/Archive/
fi

if [ -f $fCBC ] && [ -s $fCBC ]; then
	sudo rm /var/www/html/Current/CBCNews_Scrape.csv &&
	sudo cp $fCBC /var/www/html/Current/ &&
	sudo mv $fCBC /var/www/html/Archive/
fi

if [ -f $fCTV ] && [ -s $fCTV ]; then
	sudo rm /var/www/html/Current/CTVNews_Scrape.csv &&
	sudo cp $fCTV /var/www/html/Current/ &&
	sudo mv $fCTV /var/www/html/Archive/
fi

if [ -f $fGM ] && [ -s $fGM ]; then
	sudo rm /var/www/html/Current/GlobeMail_Scrape.csv &&
	sudo cp $fGM /var/www/html/Current/ &&
	sudo mv $fGM /var/www/html/Archive/
fi

if [ -f $fOC ] && [ -s $fOC ]; then
	sudo rm /var/www/html/Current/OttawaCitizen_Scrape.csv &&
	sudo cp $fOC /var/www/html/Current/ &&
	sudo mv $fOC /var/www/html/Archive/
fi

if [ -f $fTST ] && [ -s $fTST ]; then
	sudo rm /var/www/html/Current/TorontoStar_Scrape.csv &&
	sudo cp $fTST /var/www/html/Current/ &&
	sudo mv $fTST /var/www/html/Archive/
fi

if [ -f $fTSu ] && [ -s $fTSu ]; then
	sudo rm /var/www/html/Current/TorontoSun_Scrape.csv &&
	sudo cp $fTSu /var/www/html/Current/ &&
	sudo mv $fTSu /var/www/html/Archive/
fi

if [ -f $fVS ] && [ -s $fVS ]; then
	sudo rm /var/www/html/Current/VancouverSun_Scrape.csv &&
	sudo cp $fVS /var/www/html/Current/ &&
	sudo mv $fVS /var/www/html/Archive/
fi

sudo rename 's/ *[0-9]{8}_//' /var/www/html/Current/*.csv
