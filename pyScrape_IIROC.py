##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 4/6/2016
##Program Name  : pyScrape_IIROC
##Description   : Gather the names from the PDF headers on the IIROC website
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: 
##Prereqs Software: Python, pip, Python-Dev
##          Unix install command "sudo apt-get install"
##Python Libraries: LXML, requests, csv, re, datetime, numpy, nltk (numpy is prereq)
##          Unix install python lib command: "sudo pip install"
##Python file: pyTimer.py
##Log file: pylog_IIROC.txt
##Run command: sudo python pyScrape_IIROC.py
##Static variables: '/Logs/pylog_IIROC.txt'
##                  header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       04/06/2016    Justin Suelflow	Initial Draft
##   1.1      04/12/2016    Justin Suelflow     Updated scrape to take out unneccessary code
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
##  pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
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
    logFile = open('/Logs/pylog_IIROC.txt','a')
    logFile.write(text)
##  Close log file
    logFile.close()

##  Function	: createCSV
##  Description	: Writes list to a CSV file
##  Parameters	: liCSV = list type, f1 = file type
##  Returns	:
def createCSV(liCSV, f1):
    writeToLog("Writing to CSV\n")
##  Use the ^ as a delimiter because the data on Leafly has lots of other special characters including commas
##  Needed to find a special character that was not used by the data
    writer = csv.writer(f1, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
##  Add a header row to the CSV
    writer.writerow(["Name","Link"])
##  Loop through all elements in the list
    for i in liCSV:
        rowStr = ''
##  Some elements are lists so it is needed to loop through each element again
        for e in i:
	    rowStr = rowStr + str(e)
            rowStr = rowStr + ','
##  Take the last ^ off of the rowStr to finish the row
        rowStr = rowStr[:-1]
##  Write the row to the CSV file
        writer.writerow([rowStr])

##  Function	: scrapeInfo
##  Description	: Scrapes HTML content from all articles from mainContent
##  Parameters	: mainContent = string type, mainXPath = string type, paraXPath = string type
##  Returns	: list
def scrapeInfo(mainContent, mainXPath):
    li = []
    currDate = datetime.now()
    mainLinksXPath = mainContent.xpath(mainXPath)
    linkXPath = []
    for mainLinksElements in mainLinksXPath:
        link = tostring(mainLinksElements)
        link = html.fromstring(link)
        link = link.xpath('//a')
        if len(link) > 0:
            text = link[0].text
            link = link[0].get('href')
            strCond = '/Documents/' + str(currDate.year)
            if strCond in link:
                if u'\u2013' in text:
                    text = text[17:text.index(u'\u2013')]
                    link = "http://www.iiroc.ca" + link
                    li.append([text,link])
    return li

##*********************MAIN FUNCTION*********************##
##  Function	: main
##  Description	: Opens file, http request mainURL and call other functions
##  Parameters	: mainURLList = list type
##  Returns	:
def main(mainURL, mainXPath, fileName):
    with open(fileName,'w') as scrapeFile:
        nameLi = []
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        mainRequest = requests.get(mainURL, headers=header)
        mainContent = html.fromstring(mainRequest.content)
        writeToLog("Scraping URL: " + mainURL + "\n")
        nameLi = scrapeInfo(mainContent, mainXPath)
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
    fileName = '/Scrapes/' + fileDate + '_IIROC_Scrape.csv'
    mainURL = 'http://www.iiroc.ca/industry/enforcement/Pages/Enforcement.aspx'
    mainXPath = '//*[@class="ms-vb"]'
    main(mainURL, mainXPath, fileName)
##  Find total time in seconds of program run
    pName = os.path.basename(__file__)
    endTime = pyTimer.endTimer(startTime, pName)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
