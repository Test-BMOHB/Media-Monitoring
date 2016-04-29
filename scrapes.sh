#!/bin/bash

fRT="/var/www/html/Logs/pylog_Runtimes.txt"

if [ -f $fRT ] ;
then
	sudo sed -i '$a ***************************`date +\%m\%d\%Y`***************************' $fRT
else
	sudo echo '***************************`date +\%m\%d\%Y`***************************' > $fRT
fi

sudo python /var/www/html/Scrapes/pyScrape_Backpage.py >> /var/www/html/Logs/pylog_Backpage.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_NationalPost.py >> /var/www/html/Logs/pylog_NationalPost.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_PotLocator.py >> /var/www/html/Logs/pylog_PotLocator.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_MontrealGazette.py >> /var/www/html/Logs/pylog_MontrealGazette.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_GoogleNewsPanama.py >> /var/www/html/Logs/pylog_GoogleNewsPanama.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_Fintrac.py >> /var/www/html/Logs/pylog_Fintrac.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_GlobeMail.py >> /var/www/html/Logs/pylog_GlobeMail.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_CRA.py >> /var/www/html/Logs/pylog_CRA.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_GoogleNews.py >> /var/www/html/Logs/pylog_GoogleNews.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_WeedMaps.py >> /var/www/html/Logs/pylog_WeedMaps.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_Leafly.py >> /var/www/html/Logs/pylog_Leafly.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_OttawaCitizen.py >> /var/www/html/Logs/pylog_OttawaCitizen.txt 2>&1 ;
sudo python /var/www/html/Scrapes/pyScrape_CBSA.py >> /var/www/html/Logs/pylog_CBSA.txt 2>&1

sudo sed -i '$a \ ' /var/www/html/Logs/pylog_Runtimes.txt
