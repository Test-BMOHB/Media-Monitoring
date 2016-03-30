##*********************HEADER*********************##
##Developer     : Ivana Donevska
##Date          : 3/18/2016
##Program Name  : pyScrape_CBSA
##Description   : Loop through latest news section in the Canada Border Services Agency (CBSA) website
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: 
##Prereqs Software: Python, pip, Python-Dev
##          Unix install command "sudo apt-get install"
##Python Libraries: LXML, requests, csv, re, datetime, numpy, nltk (numpy is prereq)
##          Unix install python lib command: "sudo pip install"
##Python file: pyTimer.py
##Log file: pylog_GoogleNews.txt
##Run command: sudo python pyScrape_CBSA.py
##Static variables: '/var/www/html/pylog_CBSA.txt'
##                  header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       03/18/2016    Ivana Donevska	Copy py_Scrape_GoogleNews from Justin and make updates
##   1.1      03/30/2016    Justin Suelflow     Updated CSV writer to take out quotes
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
##  pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time, nltk, numpy, pyTimer
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
    logFile = open('/var/www/html/pylog_CBSA.txt','a')
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
def scrapeInfo(mainContent, mainXPath, paraXPath):
    li = []
    currDate = datetime.now()
    mainLinksXPath = mainContent.xpath(mainXPath)
    linkXPath = []
    for mainLinksElements in mainLinksXPath:
        link = tostring(mainLinksElements)
        link = html.fromstring(link)    
        link = link.xpath('//a')
        link = link[0].get('href')
        linkRequest = requests.get(link)
        linkXPath = html.fromstring(linkRequest.content) 
        linkXPath = linkXPath.xpath('//id')
    linkXPath = list(set(linkXPath))
    for i in linkXPath:
        print i.text
        writeToLog("Gathering Names from: " + i.text + "\n")
        iRequest = requests.get(i.text)
        linkContent = html.fromstring(iRequest.content)
        linkXPath2 = linkContent.xpath(paraXPath)
        pageContent = ''
        for linkXElement in linkXPath2:
            text = tostring(linkXElement)
            icons = re.findall(r'&#\d*;', text)
            icons = list(set(icons))
            for icon in icons:
                text = re.sub(icon, '', text)
            tags = re.findall('<[^>]+>', text)
            tags = list(set(tags))
            for tag in tags:
                text = text.replace(tag, '')
            pageContent = pageContent + text
            li.append([pageContent,link])
    return li

##  Function	: extractNames
##  Description	: Extracts names from html in list
##  Parameters	: li = list type
##  Returns	: list
def extractNames(li):
    finList = []
    for a in li:
        for send in nltk.sent_tokenize(str(a)):
            smLi = []
            for index, chunk in enumerate(nltk.pos_tag(nltk.word_tokenize(send))):
                if 'NNP' in chunk[1]:
                    if(len(' '.join(e for e in chunk[0] if e.isalnum())) > 2):
                        smLi.append([index, chunk, a[1]])
            finList.append(smLi)
    nameLi = []
    for f in finList:
        if len(f) > 0:
            strName = ''
            for index, i in enumerate(f):
                if strName == '':
                    strName = i[1][0]
                if (index + 1) < len(f):
                    if i[0] + 1 == f[index + 1][0]:
                        strName = strName + ' ' + f[index + 1][1][0]
                    else:
                        if ' ' in strName:
                            nameLi.append([strName, i[2]])
                        strName = ''
    return nameLi

##*********************MAIN FUNCTION*********************##
##  Function	: main
##  Description	: Opens file, http request mainURL and call other functions
##  Parameters	: mainURLList = list type
##  Returns	:
def main(mainURL, mainXPath, paraXPath, fileName):
    with open(fileName,'w') as scrapeFile:
        nameLi = []
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        url =  mainURL
        mainRequest = requests.get(url, headers=header)
        mainContent = html.fromstring(mainRequest.content)
        writeToLog("Scraping URL: " + url + "\n")
        htmlLi = scrapeInfo(mainContent, mainXPath, paraXPath)
        writeToLog("Extracting Names\n")
        nameLi.extend(extractNames(htmlLi))    
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
    try:
        punktDL = nltk.download('punkt')
        aptDL = nltk.download('averaged_perceptron_tagger')
    except:
        writeToLog('NLTK Punkt and Averaged_Perceptron_tagger need to be installed')
    currDate = datetime.now()
    fileDate = currDate.strftime('%m%d%Y')
    writeToLog('*****************************' + fileDate + '*****************************')
    fileName = '/var/www/html/' + fileDate + '_CBSA_Scrape.csv'
    mainURL = 'http://www.cbsa-asfc.gc.ca/media/menu-eng.html'
    mainXPath = '//*[@class="widget-content"]'
    paraXPath = '//p'
    if punktDL and aptDL:
        main(mainURL, mainXPath, paraXPath, fileName)
    else:
        writeToLog('NLTK Punkt and Averaged_Perceptron_tagger need to be downloaded first.')
        writeToLog('Please sudo python and run nltk.download("punkt") and nltk.download("averaged_perceptron_tagger")')
##  Find total time in seconds of program run
    endTime = pyTimer.endTimer(startTime)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
