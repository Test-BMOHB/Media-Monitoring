#!/bin/bash
##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 5/4/2016
##Program Name  : load.sh
##Description   : Runs python pyAllScrapesLoad file then loads the files created from that python code to Big Query
##Prereqs Knowledge: Unix Bash scripting, Big Query command line
##Prereqs Hardware: Unix VM
##Prereqs Software: bq
##Run command: sudo bash load.sh
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       05/04/2016    Justin Suelflow    Initial Version
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##
# Run the python file to create Big Query load files and save output to the Log files
# 2>&1 means to move the standard output and error output of the scrapes to the logs
sudo python /var/www/html/BQ/pyAllScrapesLoad.py >> /var/www/html/Logs/pylog_CombineScrapes.txt 2>&1
# Create file variables for where they are located on the VM
fBP="/var/www/html/Current/ScreenScrape_Load.csv"
fWM="/var/www/html/Current/Weedmaps_MMJScrape_Load.csv"
fL="/var/www/html/Current/Leafly_MMJScrape_Load.csv"
fPL="/var/www/html/Current/PotLocator_MMJScrape_Load.csv"
fF="/var/www/html/Current/Fintrac_Scrape_Load.csv"
fCRA="/var/www/html/Current/CRA_Scrape_Load.csv"
fCBSA="/var/www/html/Current/CBSA_Scrape_Load.csv"
fGN="/var/www/html/Current/GoogleNews_Scrape_Load.csv"
fMG="/var/www/html/Current/MontrealGazette_Scrape_Load.csv"
fGNP="/var/www/html/Current/GoogleNewsPanama_Scrape_Load.csv"
fNP="/var/www/html/Current/NationalPost_Scrape_Load.csv"
fCH="/var/www/html/Current/CalgaryHerald_Scrape_Load.csv"
fCBC="/var/www/html/Current/CBCNews_Scrape_Load.csv"
fCTV="/var/www/html/Current/CTVNews_Scrape_Load.csv"
fGM="/var/www/html/Current/GlobeMail_Scrape_Load.csv"
fOC="/var/www/html/Current/OttawaCitizen_Scrape_Load.csv"
fTST="/var/www/html/Current/TorontoStar_Scrape_Load.csv"
fTSu="/var/www/html/Current/TorontoSun_Scrape_Load.csv"
fVS="/var/www/html/Current/VancouverSun_Scrape_Load.csv"
fIR="/var/www/html/Current/IIROC_Scrape_Load.csv"
fTT="/var/www/html/Current/TopTen_Scrape_Load.csv"
# If files exist (-f) and are not empty (-s), then load the files to the Big Query table bmo_web_crawler.AllScrapes
# Skip the leading header row
# Use a comma as the delimiter
# Use the schema.txt file as the Big Query load schema
if [ -f $fBP ] && [ -s $fBP ]; then
	sudo bq load  --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fBP /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi
# Use a carat as the delimiter
if [ -f $fWM ] && [ -s $fWM ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter='^' --max_bad_records=5 bmo_web_crawler.AllScrapes $fWM /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fL ] && [ -s $fL ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter='^' --max_bad_records=5 bmo_web_crawler.AllScrapes $fL /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fPL ] && [ -s $fPL ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter='^' --max_bad_records=5 bmo_web_crawler.AllScrapes $fPL /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fF ] && [ -s $fF ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fF /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fCRA ] && [ -s $fCRA ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fCRA /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fCBSA ] && [ -s $fCBSA ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fCBSA /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fGN ] && [ -s $fGN ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fGN /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fMG ] && [ -s $fMG ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fMG /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fGNP ] && [ -s $fGNP ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fGNP /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fNP ] && [ -s $fNP ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fNP /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fCH ] && [ -s $fCH ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fCH /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fCBC ] && [ -s $fCBC ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fCBC /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fCTV ] && [ -s $fCTV ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fCTV /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fGM ] && [ -s $fGM ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fGM /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fOC ] && [ -s $fOC ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fOC /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fTST ] && [ -s $fTST ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fTST /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fTSu ] && [ -s $fTSu ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fTSu /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fVS ] && [ -s $fVS ]; then
	sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fVS /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fIR ] && [ -s $fIR ]; then
        sudo bq load --quote='' --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fIR /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi

if [ -f $fTT ] && [ -s $fTT ]; then
        sudo bq load  --skip_leading_rows=1 --field_delimiter=',' --max_bad_records=5 bmo_web_crawler.AllScrapes $fTT /var/www/html/BQ/schema.txt >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1
fi
# Run a Big Query query to overwrite the bmo_web_crawler.AllScrapesNoDup table with the deduplicated data from the bmo_web_crawler.AllScrapes table
sudo bq query --destination_table=bmo_web_crawler.AllScrapesNoDup --replace --quiet "SELECT Name, Company, PhoneNumber, EmailAddress, Address, City, State, ZipCode, Website, COUNT(*) as NumOfDups FROM bmo_web_crawler.AllScrapes GROUP BY Name, Company, PhoneNumber, EmailAddress, Address, City, State, ZipCode, Website" >> /var/www/html/Logs/pylog_LoadScrapes.txt 2>&1 ;
# Remove all of the Load CSV files from the Current directory
sudo rm /var/www/html/Current/*_Load.csv