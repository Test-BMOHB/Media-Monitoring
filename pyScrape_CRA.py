##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 3/28/2016
##Program Name  : pyScrape_CRA
##Description   : Review recent articles listed across the prvince and territory links
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath, NLTK
##Prereqs Hardware: 
##Prereqs Software: Python, pip, Python-Dev
##          Unix install command "sudo apt-get install"
##Python Libraries: LXML, requests, csv, re, datetime, numpy, os, nltk (numpy is prereq for nltk)
##          Unix install python lib command: "sudo pip install"
##Needed Python file: pyTimer.py
##          pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
##Log file saved at: /var/www/html/Logs/pylog_CRA.txt
##CSV file saved at: /var/www/html/mmddyyyy_CRA_Scrape.csv
##Run command: sudo python pyScrape_CRA.py
##Static variables: header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       03/28/2016    Justin Suelflow    Initial Version to grab names from articles
##   1.1      03/30/2016    Justin Suelflow    Updated CSV writer to take out quotes
##   1.2      03/31/2016    Justin Suelflow    Added filename var to send to pyTimer
##   1.3      04/11/2016    Justin Suelflow    Changed log file path
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
##  pyTimer is not installed using pip, the standalone file needs to be placed in the same location as this code file
from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time, nltk, numpy, pyTimer, os.path
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
    logFile = open('/var/www/html/Logs/pylog_CRA.txt','a')
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
##  Take the last comma off of the rowStr to finish the row
        rowStr = rowStr[:-1]
##  Write the row to the CSV file
        writer.writerow([rowStr])

##  Function	: scrapeInfo
##  Description	: Scrapes HTML content from all articles from mainContent
##  Parameters	: mainContent = string type, mainXPath = string type, paraXPath = string type
##  Returns	: list
def scrapeInfo(mainContent, mainXPath, linkXPath, paraXPath):
    li = []
    mainLinksXPath = mainContent.xpath(mainXPath)
    mainLinksXPath = list(set(mainLinksXPath))
    for mainLinksElements in mainLinksXPath:
        link = tostring(mainLinksElements)
        link = html.fromstring(link)
        link = link.xpath('//a')
        for i in link:
            i = i.get('href')
            if 'http' not in i:
                i = 'http://www.cra-arc.gc.ca' + i
##  Do a HTTP request on the article link
            linkRequest = requests.get(i)
            linkContent = html.fromstring(linkRequest.content)
##  Find the paraXpath in the article
            lXPath = linkContent.xpath(linkXPath)
            for linkXElement in lXPath:
                text = tostring(linkXElement)
                text = html.fromstring(text)
                text = text.xpath('//a')
                for a in text:
                    a = tostring(a)
                    a = html.fromstring(a)
                    a = a.get('href')
                    a = 'http://www.cra-arc.gc.ca' + a
                    aRequest = requests.get(a)
                    aContent = html.fromstring(aRequest.content)
                    aXPath = aContent.xpath(paraXPath)
                    pageContent = ''
                    writeToLog("Gathering Names from: " + a + "\n")
                    for x in aXPath:
                        x = tostring(x)
##  Delete all icons and small emojis from HTML text
                        icons = re.findall(r'&#\d*;', x)
                        icons = list(set(icons))
                        for icon in icons:
                            x = re.sub(icon, '', x)
##  Delete all HTML tags from HTML text
                        tags = re.findall('<[^>]+>', x)
                        tags = list(set(tags))
                        for tag in tags:
                            x = x.replace(tag, '')
                        pageContent = pageContent + x
##  Add HTML content and the article link to a list
                    li.append([pageContent,a])
    return li

##  Function	: extractNames
##  Description	: Extracts names from html in list
##  Parameters	: li = list type
##  Returns	: list
def extractNames(li):
    finList = []
##  Loop through the list that has the HTML page content
    for a in li:
##  Tokenize the HTML text into smaller blocks of text
        for send in nltk.sent_tokenize(str(a)):
            smLi = []
##  Tokenize the smaller blocks of text in individual words and then add a Part-of-Speech(POS) tag
            for index, chunk in enumerate(nltk.pos_tag(nltk.word_tokenize(send))):
##  If the POS tag is NNP (noun)
                if 'NNP' in chunk[1]:
##  If the each character in the word is an alphanumeric character and there are more than 2 characters in the word
                    if(len(' '.join(e for e in chunk[0] if e.isalnum())) > 2):
##  Append the list with the index of the word, chunk that has the POS tag and the link
                        smLi.append([index, chunk, a[1]])
            finList.append(smLi)
    nameLi = []
    for f in finList:
        if len(f) > 0:
            strName = ''
            for index, i in enumerate(f):
##  If strName is blank, declare it with the current word in the list
                if strName == '':
                    strName = i[1][0]
##  If index+1 is not at the end of the list, continue
                if (index + 1) < len(f):
##  If the index is a consecutive index, add to the strName
                    if i[0] + 1 == f[index + 1][0]:
                        strName = strName + ' ' + f[index + 1][1][0]
##  If the index is not a consecutive index, append strName to the nameLi list with the article link and make the strName blank
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
def main(mainURL, mainXPath, linkXPath, paraXPath, fileName):
##  Automatically creates file if it does not exist
    with open(fileName,'w') as scrapeFile:
        nameLi = []
        header = {'User-Agent': 'Mozilla/Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        mainRequest = requests.get(mainURL, headers=header)
##  Translate mainRequest content into HTML
        mainContent = html.fromstring(mainRequest.content)
        htmlLi = scrapeInfo(mainContent, mainXPath, linkXPath, paraXPath)
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
##  Try to download NLTK packages
    try:
        punktDL = nltk.download('punkt')
        aptDL = nltk.download('averaged_perceptron_tagger')
    except:
        writeToLog('NLTK Punkt and Averaged_Perceptron_tagger need to be installed')
    currDate = datetime.now()
    fileDate = currDate.strftime('%m%d%Y')
    writeToLog('*****************************' + fileDate + '*****************************\n')
    fileName = '/var/www/html/' + fileDate + '_CRA_Scrape.csv'
    mainURL = 'http://www.cra-arc.gc.ca/convictions/'
    mainXPath = '//*[@class="module-menu-section span-3"]'
    linkXPath = '//*[@class="col-md-9 col-md-push-3"]'
    paraXPath = '//p'
## If the NLTK packages are downloaded, run the main program
    if punktDL and aptDL:
        main(mainURL, mainXPath, linkXPath, paraXPath, fileName)
    else:
        writeToLog('NLTK Punkt and Averaged_Perceptron_tagger need to be downloaded first.')
        writeToLog('Please sudo python and run nltk.download("punkt") and nltk.download("averaged_perceptron_tagger")')
##  Find total time in seconds of program run
    pName = os.path.basename(__file__)
    endTime = pyTimer.endTimer(startTime, pName)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
