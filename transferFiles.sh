#!/bin/bash
##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 5/4/2016
##Program Name  : transferFiles.sh
##Description   : Moves files from other VMs that run scrapes to the VM that runs this file. Then copies those files to the Current directory
##Prereqs Knowledge: Unix Bash scripting, gcloud command line
##Prereqs Hardware: Unix VM
##Prereqs Software: gcloud
##Run command: sudo bash transferFiles.sh
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       05/04/2016    Justin Suelflow    Initial Version
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##
# Create file variables for where they are located on the VM
fCH="`date +\%m\%d\%Y`_CalgaryHerald_Scrape.csv"
fCBC="`date +\%m\%d\%Y`_CBCNews_Scrape.csv"
fCTV="`date +\%m\%d\%Y`_CTVNews_Scrape.csv"
fTST="`date +\%m\%d\%Y`_TorontoStar_Scrape.csv"
fTSu="`date +\%m\%d\%Y`_TorontoSun_Scrape.csv"
fVS="`date +\%m\%d\%Y`_VancouverSun_Scrape.csv"
fIR="`date +\%m\%d\%Y`_IIROC_Scrape.csv"
fTT="`date +\%m\%d\%Y`_TopTen_Scrape.csv"
# Copy scrape files from the other VMs to the current VM's Archive directory
sudo gcloud compute copy-files instance-webapp1:/Scrapes/$fCH /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp1:/Scrapes/$fCBC /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp1:/Scrapes/$fCTV /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp3:/Scrapes/$fTST /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp3:/Scrapes/$fTSu /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp3:/Scrapes/$fVS /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp4:/Scrapes/$fIR /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp4:/Scrapes/$fTT /var/www/html/Archive --zone us-central1-a
# Copy the files from the Archive directory copy them into the Current directory
sudo cp /var/www/html/Archive/$fCH /var/www/html/Current/CalgaryHerald_Scrape.csv
sudo cp /var/www/html/Archive/$fCBC /var/www/html/Current/CBCNews_Scrape.csv
sudo cp /var/www/html/Archive/$fCTV /var/www/html/Current/CTVNews_Scrape.csv
sudo cp /var/www/html/Archive/$fTST /var/www/html/Current/TorontoStar_Scrape.csv
sudo cp /var/www/html/Archive/$fTSu /var/www/html/Current/TorontoSun_Scrape.csv
sudo cp /var/www/html/Archive/$fVS /var/www/html/Current/VancouverSun_Scrape.csv
sudo cp /var/www/html/Archive/$fIR /var/www/html/Current/IIROC_Scrape.csv
sudo cp /var/www/html/Archive/$fTT /var/www/html/Current/TopTen_Scrape.csv
