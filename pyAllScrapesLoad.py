import csv, traceback, os.path
from datetime import datetime
cDate = datetime.now()
fileDate = cDate.strftime('%m%d%Y')
cDate = cDate.strftime('%m/%d/%Y')
def createLoadFile(filename, loadfile, delimit, cDate, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, scrape):
    try:
        li = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=delimit)
            head = reader.next()
            head = ['Date','Name','Company','PhoneNumber','Email_Address','Address','City','State','ZipCode','Website','Link','Scrape']
            li.append(head)
            for r in reader:
                row = [cDate]
                if r1 == '':
                    row.append('')
                else:
                    row.append(r[r1])
                if r2 == '':
                    row.append('')
                else:
                    row.append(r[r2])
                if r3 == '':
                    row.append('')
                else:
                    row.append(r[r3])
                if r4 == '':
                    row.append('')
                else:
                    row.append(r[r4])
                if r5 == '':
                    row.append('')
                else:
                    row.append(r[r5])
                if r6 == '':
                    row.append('')
                else:
                    row.append(r[r6])
                if r7 == '':
                    row.append('')
                else:
                    row.append(r[r7])
                if r8 == '':
                    row.append('')
                else:
                    row.append(r[r8])
                if r9 == '':
                    row.append('')
                else:
                    row.append(r[r9])
                if r10 == '':
                    row.append('')
                else:
                    row.append(r[r10])
                row.append(scrape)
                li.append(row)
        if len(li) > 0:
            out = open(loadfile, 'w')
            writer = csv.writer(out, delimiter=delimit)
            writer.writerows(li)
            out.close()
    except:
        e = traceback.format_exc()
        print scrape + " did not translate properly\nUnexpected Error: " + str(e) + "\n"

fGN="/var/www/html/Archive/" + fileDate + "_GoogleNews_Scrape.csv"
fGNP="/var/www/html/Archive/" + fileDate + "_GoogleNewsPanama_Scrape.csv"
fCBSA="/var/www/html/Archive/" + fileDate + "_CBSA_Scrape.csv"
fCRA="/var/www/html/Archive/" + fileDate + "_CRA_Scrape.csv"
fF="/var/www/html/Archive/" + fileDate + "_Fintrac_Scrape.csv"
fPL="/var/www/html/Archive/" + fileDate + "_PotLocator_MMJScrape.csv"
fWM="/var/www/html/Archive/" + fileDate + "_Weedmaps_MMJScrape.csv"
fBP="/var/www/html/Archive/" + fileDate + "_ScreenScrape.csv"
fL="/var/www/html/Archive/" + fileDate + "_Leafly_MMJScrape.csv"
fMG="/var/www/html/Archive/" + fileDate + "_MontrealGazette_Scrape.csv"
fCH="/var/www/html/Archive/" + fileDate + "_CalgaryHerald_Scrape.csv"
fCBC="/var/www/html/Archive/" + fileDate + "_CBCNews_Scrape.csv"
fCTV="/var/www/html/Archive/" + fileDate + "_CTVNews_Scrape.csv"
fGM="/var/www/html/Archive/" + fileDate + "_GlobeMail_Scrape.csv"
fNP="/var/www/html/Archive/" + fileDate + "_NationalPost_Scrape.csv"
fOC="/var/www/html/Archive/" + fileDate + "_OttawaCitizen_Scrape.csv"
fTST="/var/www/html/Archive/" + fileDate + "_TorontoStar_Scrape.csv"
fTSu="/var/www/html/Archive/" + fileDate + "_TorontoSun_Scrape.csv"
fVS="/var/www/html/Archive/" + fileDate + "_VancouverSun_Scrape.csv"

if os.path.isfile(fGN):
    if os.path.getsize(fGN) > 0:
	createLoadFile(fGN, '/var/www/html/Current/GoogleNews_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Google News')

if os.path.isfile(fGNP):
    if os.path.getsize(fGNP) > 0:
	createLoadFile(fGNP, '/var/www/html/Current/GoogleNewsPanama_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Google News Panama')

if os.path.isfile(fCBSA):
    if os.path.getsize(fCBSA) > 0:
	createLoadFile(fCBSA, '/var/www/html/Current/CBSA_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CBSA')

if os.path.isfile(fCRA):
    if os.path.getsize(fCRA) > 0:
	createLoadFile(fCRA, '/var/www/html/Current/CRA_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CRA')

if os.path.isfile(fF):
    if os.path.getsize(fF) > 0:
	createLoadFile(fF, '/var/www/html/Current/Fintrac_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Fintrac')

if os.path.isfile(fPL):
    if os.path.getsize(fPL) > 0:
	createLoadFile(fPL, '/var/www/html/Current/PotLocator_MMJScrape_Load.csv', '^', cDate, '', 0, 1, '', 2, 3, 4, 5, 6, '', 'PotLocator')

if os.path.isfile(fWM):
    if os.path.getsize(fWM) > 0:
	createLoadFile(fWM, '/var/www/html/Current/Weedmaps_MMJScrape_Load.csv', '^', cDate, '', 0, 1, '', 2, 3, 4, 5, 6, '', 'Weedmaps')

if os.path.isfile(fBP):
    if os.path.getsize(fBP) > 0:
	createLoadFile(fBP, '/var/www/html/Current/ScreenScrape_Load.csv', ',', cDate, '', '', 0, 1, '', '', '', '', 2, 3, 'Backpage')

if os.path.isfile(fL):
    if os.path.getsize(fL) > 0:
	createLoadFile(fL, '/var/www/html/Current/Leafly_MMJScrape_Load.csv', '^', cDate, '', 0, 1, '', 2, 3, 4, 5, 6, 7, 'Leafly')

if os.path.isfile(fMG):
    if os.path.getsize(fMG) > 0:
	createLoadFile(fMG, '/var/www/html/Current/MontrealGazette_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Montreal Gazette')

if os.path.isfile(fCH):
    if os.path.getsize(fCH) > 0:
	createLoadFile(fCH, '/var/www/html/Current/CalgaryHerald_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Calgary Herald')

if os.path.isfile(fCBC):
    if os.path.getsize(fCBC) > 0:
	createLoadFile(fCBC, '/var/www/html/Current/CBCNews_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CBC News')

if os.path.isfile(fCTV):
    if os.path.getsize(fCTV) > 0:
	createLoadFile(fCTV, '/var/www/html/Current/CTVNews_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'CTV News')

if os.path.isfile(fGM):
    if os.path.getsize(fGM) > 0:
	createLoadFile(fGM, '/var/www/html/Current/GlobeMail_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Globe and Mail')

if os.path.isfile(fNP):
    if os.path.getsize(fNP) > 0:
	createLoadFile(fNP, '/var/www/html/Current/NationalPost_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'National Post')

if os.path.isfile(fOC):
    if os.path.getsize(fOC) > 0:
	createLoadFile(fOC, '/var/www/html/Current/OttawaCitizen_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Ottawa Citizen')

if os.path.isfile(fTST):
    if os.path.getsize(fTST) > 0:
	createLoadFile(fTST, '/var/www/html/Current/TorontoStar_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Toronto Star')

if os.path.isfile(fTSu):
    if os.path.getsize(fTSu) > 0:
	createLoadFile(fTSu, '/var/www/html/Current/TorontoSun_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Toronto Sun')

if os.path.isfile(fVS):
    if os.path.getsize(fVS) > 0:
	createLoadFile(fVS, '/var/www/html/Current/VancouverSun_Scrape_Load.csv', ',', cDate, 0, '', '', '', '', '', '', '', '', 1, 'Vancouver Sun')
