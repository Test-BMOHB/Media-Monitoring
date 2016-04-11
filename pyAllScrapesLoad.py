import csv, traceback
from datetime import datetime
cDate = datetime.now()
cDate = cDate.strftime('%m/%d/%Y')
def createLoadFile(filename, loadfile, delimit, cDate, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, scrape):
    try:
        with open(filename, 'r') as f:
            with open(loadfile, 'w') as out:
                reader = csv.reader(f, delimiter=delimit)
                writer = csv.writer(out, delimiter=delimit)
                head = reader.next()
                head = ['Date','Name','Company','PhoneNumber','Email_Address','Address','City','State','ZipCode','Website','Link','Scrape']
                li = []
                li.append(head)
                for r in reader:
                    r = [cDate]
                    if r1 == '':
                        r.append('')
                    else:
                        r.append(r[r1])
                    if r2 == '':
                        r.append('')
                    else:
                        r.append(r[r2])
                    if r3 == '':
                        r.append('')
                    else:
                        r.append(r[r3])
                    if r4 == '':
                        r.append('')
                    else:
                        r.append(r[r4])
                    if r5 == '':
                        r.append('')
                    else:
                        r.append(r[r5])
                    if r6 == '':
                        r.append('')
                    else:
                        r.append(r[r6])
                    if r7 == '':
                        r.append('')
                    else:
                        r.append(r[r7])
                    if r8 == '':
                        r.append('')
                    else:
                        r.append(r[r8])
                    if r9 == '':
                        r.append('')
                    else:
                        r.append(r[r9])
                    if r10 == '':
                        r.append('')
                    else:
                        r.append(r[r10])
                    r.append(scrape)
                    li.append(r)
                writer.writerows(li)
    except:
        e = traceback.format_exc()
        print scrape + " did not translate properly\nUnexpected Error: " + str(e) + "\n"

##  Google News
createLoadFile('/var/www/html/Current/GoogleNews_Scrape.csv', '/var/www/html/Current/GoogleNews_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Google News')
##  Google News Panama
createLoadFile('/var/www/html/Current/GoogleNewsPanama_Scrape.csv', '/var/www/html/Current/GoogleNewsPanama_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Google News Panama')
##  CBSA
createLoadFile('/var/www/html/Current/CBSA_Scrape.csv', '/var/www/html/Current/CBSA_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CBSA')
##  CRA
createLoadFile('/var/www/html/Current/CRA_Scrape.csv', '/var/www/html/Current/CRA_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CRA')
##  Fintrac
createLoadFile('/var/www/html/Current/Fintrac_Scrape.csv', '/var/www/html/Current/Fintrac_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Fintrac')
##  PotLocator
createLoadFile('/var/www/html/Current/PotLocator_MMJScrape.csv', '/var/www/html/Current/PotLocator_MMJScrape_Load.csv', '^', cDate, '', 0, 1, '', 2, 3, 4, 5, 6, '', 'PotLocator')
##  Weedmaps
createLoadFile('/var/www/html/Current/Weedmaps_MMJScrape.csv', '/var/www/html/Current/Weedmaps_MMJScrape_Load.csv', '^', cDate, '', 0, 1, '', 2, 3, 4, 5, 6, '', 'Weedmaps')
##  Backpage
createLoadFile('/var/www/html/Current/ScreenScrape.csv', '/var/www/html/Current/ScreenScrape_Load.csv', ',', cDate, '', '', 0, 1, '', '', '', '', 2, 3, 'Backpage')
##  Leafly
createLoadFile('/var/www/html/Current/Leafly_MMJScrape.csv', '/var/www/html/Current/Leafly_MMJScrape_Load.csv', '^', cDate, '', 0, 1, '', 2, 3, 4, 5, 6, 7, 'Leafly')
##  Montreal Gazette
createLoadFile('/var/www/html/Current/MontrealGazette_Scrape.csv', '/var/www/html/Current/MontrealGazette_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Montreal Gazette')
##  Calgary Herald
createLoadFile('/var/www/html/Current/CalgaryHerald_Scrape.csv', '/var/www/html/Current/CalgaryHerald_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Calgary Herald')
##  CBC News
createLoadFile('/var/www/html/Current/CBCNews_Scrape.csv', '/var/www/html/Current/CBCNews_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CBC News')
##  CTV News
createLoadFile('/var/www/html/Current/CTVNews_Scrape.csv', '/var/www/html/Current/CTVNews_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CTV News')
##  Globe and Mail
createLoadFile('/var/www/html/Current/GlobeMail_Scrape.csv', '/var/www/html/Current/GlobeMail_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Globe and Mail')
##  National Post
createLoadFile('/var/www/html/Current/NationalPost_Scrape.csv', '/var/www/html/Current/NationalPost_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'National Post')
##  Ottawa Citizen
createLoadFile('/var/www/html/Current/OttawaCitizen_Scrape.csv', '/var/www/html/Current/OttawaCitizen_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Ottawa Citizen')
##  Toronto Star
createLoadFile('/var/www/html/Current/TorontoStar_Scrape.csv', '/var/www/html/Current/TorontoStar_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Toronto Star')
##  Toronto Sun
createLoadFile('/var/www/html/Current/TorontoSun_Scrape.csv', '/var/www/html/Current/TorontoSun_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Toronto Sun')
##  Vancouver Sun
createLoadFile('/var/www/html/Current/VancouverSun_Scrape.csv', '/var/www/html/Current/VancouverSun_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Vancouver Sun')
