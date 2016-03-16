##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 3/15/2016
##Program Name  : pyScrape_GoogleNews
##Description   : Loop through current day's articles on Google News to pull names from articles
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: 
##Prereqs Software: Python, pip, Python-Dev
##          Unix install command "sudo apt-get install"
##Python Libraries: LXML, requests, csv, re, datetime, numpy, nltk (numpy is prereq)
##          Unix install python lib command: "sudo pip install"
##Static variables: '/var/www/html/pylog_GoogleNews.txt'
##                  header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       03/14/2016    Justin Suelflow    Initial Version to grab names from current day
##    2       03/15/2016    Justin Suelflow    Added comments
##   2.1      03/16/2016    Justin Suelflow    Made portable
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
    logFile = open('/var/www/html/pylog_GoogleNews.txt','a')
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
    writer = csv.writer(f1, delimiter=',')
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
##  Make currDate 7 day's ago date
    currDate = currDate - timedelta(days=7)
    currDate = currDate.strftime('%b %d, %Y')
    currDate = time.strptime(currDate, "%b %d, %Y")
    mainLinksXPath = mainContent.xpath(mainXPath)
    mainLinksXPath = list(set(mainLinksXPath))
    for mainLinksElements in mainLinksXPath:
        link = tostring(mainLinksElements)
        link = link[(link.index("<a")):]
        link = link[(link.index("href=") + 5):]
        link = link.split()
        link = link[0]
        link = link.replace('"', '')
        date = tostring(mainLinksElements)
        date = date[(date.index("f nsa _uQb") + 12):]
        date = date[:date.index("</span>")]
        try:
            date = time.strptime(date, "%b %d, %Y")
        except:
            if 'ago' in date:
                date = datetime.now()
                date = date.strftime('%b %d, %Y')
                date = time.strptime(date, "%b %d, %Y")
        if currDate <= date:
            linkRequest = requests.get(link)
	    writeToLog("Gathering Names from: " + link + "\n")
            linkContent = html.fromstring(linkRequest.content)
            linkXPath = linkContent.xpath(paraXPath)
            pageContent = ''
            for linkXElement in linkXPath:
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
def main(mainURL, mainXPath, paraXPath, fileName, queryLi):
    with open(fileName,'w') as scrapeFile:
        nameLi = []
        for q in queryLi:
            increment = 0
            while increment < 10:
                header = {'User-Agent': 'Mozilla/Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
                url = mainURL + q
                if increment == 0:
                    mainRequest = requests.get(url, headers=header)
                else:
                    url = url + "&start=" + str(increment * 10)
                mainContent = html.fromstring(mainRequest.content)
                writeToLog("Scraping URL: " + url + "\n")
                htmlLi = scrapeInfo(mainContent, mainXPath, paraXPath)
                writeToLog("Extracting Names\n")
                nameLi.extend(extractNames(htmlLi))
		increment = increment + 1
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
    fileName = '/var/www/html/' + fileDate + '_GoogleNews_Scrape.csv'
    queryLi = ['arrest+OR+convicted+OR+guilty+OR+charged+OR+accused+AND~%22money+laundering%22']
    mainURL = 'https://www.google.ca/search?tbm=nws&source=lnt&tbs=sbd:1&q='
    mainXPath = '//*[@class="g"]'
    paraXPath = '//p'
    if punktDL and aptDL:
        main(mainURL, mainXPath, paraXPath, fileName, queryLi)
    else:
        writeToLog('NLTK Punkt and Averaged_Perceptron_tagger need to be downloaded first.')
        writeToLog('Please sudo python and run nltk.download("punkt") and nltk.download("averaged_perceptron_tagger")')
##  Find total time in seconds of program run
    endTime = pyTimer.endTimer(startTime)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
