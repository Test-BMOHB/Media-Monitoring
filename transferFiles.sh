#!/bin/bash

fCH="`date +\%m\%d\%Y`_CalgaryHerald_Scrape.csv"
fCBC="`date +\%m\%d\%Y`_CBCNews_Scrape.csv"
fCTV="`date +\%m\%d\%Y`_CTVNews_Scrape.csv"
fTST="`date +\%m\%d\%Y`_TorontoStar_Scrape.csv"
fTSu="`date +\%m\%d\%Y`_TorontoSun_Scrape.csv"
fVS="`date +\%m\%d\%Y`_VancouverSun_Scrape.csv"

sudo gcloud compute copy-files instance-webapp1:/Scrapes/$fCH /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp1:/Scrapes/$fCBC /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp1:/Scrapes/$fCTV /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp3:/Scrapes/$fTST /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp3:/Scrapes/$fTSu /var/www/html/Archive --zone us-central1-a
sudo gcloud compute copy-files instance-webapp3:/Scrapes/$fVS /var/www/html/Archive --zone us-central1-a

sudo cp /var/www/html/Archive/$fCH /var/www/html/Current/CalgaryHerald_Scrape.csv
sudo cp /var/www/html/Archive/$fCBC /var/www/html/Current/CBCNews_Scrape.csv
sudo cp /var/www/html/Archive/$fCTV /var/www/html/Current/CTVNews_Scrape.csv
sudo cp /var/www/html/Archive/$fTST /var/www/html/Current/TorontoStar_Scrape.csv
sudo cp /var/www/html/Archive/$fTSu /var/www/html/Current/TorontoSun_Scrape.csv
sudo cp /var/www/html/Archive/$fVS /var/www/html/Current/VancouverSun_Scrape.csv
