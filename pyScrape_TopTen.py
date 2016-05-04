##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 5/3/2016
##Program Name  : pyScrape_TopTen
##Description   : Gather the names from the Quebec's Top Ten Most Wanted Criminals and the Arrested Criminals
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: 
##Prereqs Software: Python, pip, Python-Dev
##          Unix install command "sudo apt-get install"
##Python Libraries: LXML, requests, csv, re, datetime, numpy, os, nltk (numpy is prereq for nltk)
##          Unix install python lib command: "sudo pip install"
##Needed Python file: pyTimer.py
##          pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
##Log file saved at: /Logs/pylog_TopTen.txt
##CSV file saved at: /Scrapes/mmddyyyy_TopTen_Scrape.csv
##Run command: sudo python pyScrape_TopTen.py
##Static variables: '/Scrapes/pylog_TopTen.txt'
##                  header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       05/03/2016    Justin Suelflow	    Initial Draft
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
##  pyTimer is not installed using pip, the standalone file needs to be placed in the same location as this code file
from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time, pyTimer, os.path
##*********************END IMPORT*********************##

##*********************FUNCTIONS*********************##
##  Function	: removeDuplicates
##  Description	: Remove exact duplicate list entries
##  Parameters	: dedup = list type
##  Returns	: list
def removeDuplicates(dedup):
    finalList = []
    for x in dedup:
        if x not in finalList:
            finalList.append(x)
    return finalList

##  Function	: writeToLog
##  Description	: Write text to log
##  Parameters	: text = string type
##  Returns	:
def writeToLog(text):
##  Open a log file and append to the end of the log
##  If no log file is in directory, this will automatically create it
    logFile = open('/Logs/pylog_TopTen.txt','a')
    logFile.write(text)
##  Close log file
    logFile.close()

##  Function	: createCSV
##  Description	: Writes list to a CSV file
##  Parameters	: liCSV = list type, f1 = file type
##  Returns	:
def createCSV(liCSV, f1):
    writeToLog("Writing to CSV\n")
##  Use the comma as a delimiter
    writer = csv.writer(f1, delimiter=',', quoting=csv.QUOTE_ALL)
##  Add a header row to the CSV
    writer.writerow(["Name","WantedOrArrested","Link"])
##  Loop through all elements in the list
    for i in liCSV:
##  Write the row to the CSV file
        writer.writerow([str(i[0].encode('utf-8')),str(i[1].encode('utf-8')),str(i[2].encode('utf-8'))])

##  Function	: scrapeInfo
##  Description	: Scrapes names from Wanted website
##  Parameters	: mainContent = string type, mainXPath = string type, paraXPath = string type
##  Returns	: list
def scrapeInfo(mainContent, mainXPath, mainURL):
    li = []
    currDate = datetime.now()
    mainLinksXPath = mainContent.xpath(mainXPath)
##  Loop through elements in mainLinksXPath
    for mainLinksElements in mainLinksXPath:
        name = tostring(mainLinksElements)
        name = html.fromstring(name)
        name = name.xpath('//h3')
        if len(name) > 0:
            name = name[0].text
            if 'index-en' in mainURL:
                li.append([name,"Wanted",mainURL])
            else:
                li.append([name,"Arrested",mainURL])
    return li

##*********************MAIN FUNCTION*********************##
##  Function	: main
##  Description	: Opens file, http request mainURL and call other functions
##  Parameters	: mainURLList = list type
##  Returns	:
def main(liMainURLs, mainXPath, fileName):
##  Automatically creates file if it does not exist
    with open(fileName,'w') as scrapeFile:
        nameLi = []
##  Set header variable to trick the http request to think a web browser is opening the page
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
##  Loop through the URLs
        for mainURL in liMainURLs:
##  Http request the mainURL with a header variable
            mainRequest = requests.get(mainURL, headers=header)
##  Translate mainRequest content into HTML
            mainContent = html.fromstring(mainRequest.content)
            writeToLog("Scraping URL: " + mainURL + "\n")
            nameLi.extend(scrapeInfo(mainContent, mainXPath, mainURL))
        writeToLog("Removing Duplicates\n")
        nameLi = removeDuplicates(nameLi)
        writeToLog("Creating CSV\n")
        createCSV(nameLi, scrapeFile)

##*********************END MAIN FUNCTION*********************##

##*********************END FUNCTIONS*********************##

##*********************PROGRAM*********************##
##  If statement makes this program standalone
##  Do not need this if statement if another program will be calling above functions
if __name__ == "__main__":
##  Create start time
    startTime = pyTimer.startTimer()
    currDate = datetime.now()
    fileDate = currDate.strftime('%m%d%Y')
    writeToLog('*****************************' + fileDate + '*****************************\n')
    fileName = '/Scrapes/' + fileDate + '_TopTen_Scrape.csv'
##  Declare list of URLs
    liMainURLs = ['http://www.10criminelsrecherches.qc.ca/index-en.html','http://www.10criminelsrecherches.qc.ca/archive-en.html','http://www.10criminelsrecherches.qc.ca/archive-en-1.html','http://www.10criminelsrecherches.qc.ca/archive-en-2.html']
    mainXPath = '//div[@class="bref"]'
    main(liMainURLs, mainXPath, fileName)
##  Find total time in seconds of program run
    pName = os.path.basename(__file__)
    endTime = pyTimer.endTimer(startTime, pName)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
