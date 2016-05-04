#!/bin/bash
# Create variable for Runtime file log
fRT="/var/www/html/Logs/pylog_Runtimes.txt"
# If file exists (-f), then add separator line to file else create a new file with separator line
if [ -f $fRT ] ;
then
	sudo sed -i '$a ***************************`date +\%m\%d\%Y`***************************' $fRT
else
	sudo echo '***************************`date +\%m\%d\%Y`***************************' > $fRT
fi
# Run python scrapes and save output to the Log files
# 2>&1 means to move the standard output and error output of the scrapes to the logs
# ; means that the next line is dependent on the current line completing regardless of failure or success
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
# Add a blank row to the file after all scrapes finish
sudo sed -i '$a \ ' /var/www/html/Logs/pylog_Runtimes.txt