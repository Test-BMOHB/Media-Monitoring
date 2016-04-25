##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 4/11/2016
##Program Name  : pyScrape_CBCNews
##Description   : Loop through last 2 days worth of CBC News articles on 10 pages of Google News to pull nouns
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: 
##Prereqs Software: Python, pip, Python-Dev
##          Unix install command "sudo apt-get install"
##Python Libraries: LXML, requests, csv, re, os, datetime, numpy, nltk (numpy is prereq for nltk)
##          Unix install python lib command: "sudo pip install"
##Needed Python file: pyTimer.py
##          pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
##Log file saved at: /Logs/pylog_CBCNews.txt
##CSV file saved at: /Scrapes/mmddyyyy_CBCNews_Scrape.csv
##Run command: sudo python pyScrape_CBCNews.py
##Static variables: '/Logs/pylog_CBCNews.txt'
##                  header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       04/11/2016    Justin Suelflow    Initial Version to grab names from current day
##   1.1      04/11/2016    Justin Suelflow    Changed log file path
##   1.2      04/12/2016    Justin Suelflow    Changed from 7 days to current day minus 1 day because runtime is long
##                                                  Changed to only look for CBC News website
##   1.3      04/12/2016    Justin Suelflow    Added code to break from page incrementing
##    2       04/13/2016    Justin Suelflow    Bug fixes (Pager not requesting new Google News pages, break when no links found)
##                                                  Add function to gather links and deduplicate links before getting HTML content
##   2.1      04/18/2016    Justin Suelflow    mainXPath change and log writing changes
##   2.2      04/19/2016    Justin Suelflow    Set serach string to pull 100 articles at once instead of default(10)
##                                                  Call scrapeinfo function inbetween GN page calls to point to other websites
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
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
    logFile = open('/Logs/pylog_CBCNews.txt','a')
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

##  Function	: gatherLinks
##  Description	: Scrapes links from the mainContent
##  Parameters	: mainContent = string type, mainXPath = string type
##  Returns	: list
def gatherLinks(mainContent, mainXPath):
    liLinks = []
    currDate = datetime.now()
##  Make currDate minus 1 day
    currDate = currDate - timedelta(days=1)
    currDate = currDate.strftime('%b %d, %Y')
    currDate = time.strptime(currDate, "%b %d, %Y")
    mainLinksXPath = mainContent.xpath(mainXPath)
    for mainLinksElements in mainLinksXPath:
        links = mainLinksElements.xpath('.//a[@class="l _HId"]')
        for link in links:
            link = link.get('href')
        d = ''
        dates = mainLinksElements.xpath('.//span[@class="f nsa _uQb"]')
        for date in dates:
            date = date.text
            try:
##  Make the date string into a time object
                d = time.strptime(date, "%b %d, %Y")
##  If the date string is not is a format that is accepted, look for 'ago' in the string. Example date string: 30 minutes ago
            except:
                if 'ago' in date:
##  Make the date string equal today's date
                    date = datetime.now()
                    date = date.strftime('%b %d, %Y')
                    d = time.strptime(date, "%b %d, %Y")
##  If the date for the link is within the timeframe, add link to the liLinks list
        if currDate <= d:
            liLinks.append(link)
        else:
            break
    liLinks = list(set(liLinks))
    return liLinks

##  Function	: scrapeInfo
##  Description	: Scrapes HTML content from all articles in list
##  Parameters	: link = string type, paraXPath = string type
##  Returns	: list
def scrapeInfo(liLinks, paraXPath):
    li = []
    for link in liLinks:
        try:
##  Do a HTTP request on the article link
            linkRequest = requests.get(link)
            linkContent = html.fromstring(linkRequest.content)
##  Find the paraXpath in the article
            linkXPath = linkContent.xpath(paraXPath)
            pageContent = ''
            for linkXElement in linkXPath:
                text = tostring(linkXElement)
##  Delete all icons and small emojis from HTML text
                icons = re.findall(r'&#\d*;', text)
                icons = list(set(icons))
                for icon in icons:
                    text = re.sub(icon, '', text)
##  Delete all HTML tags from HTML text
                tags = re.findall('<[^>]+>', text)
                tags = list(set(tags))
                for tag in tags:
                    text = text.replace(tag, '')
                htmlSyntax = ['\t','\n']
                for hs in htmlSyntax:
                    text = text.replace(hs, '')
                pageContent = pageContent + text
##  Add HTML content and the article link to a list
            li.append([pageContent,link])
        except:
                writeToLog("Link: " + link + " was not scraped due to an error.")
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
##  If strName is blank, declare it with the next word in the list
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
def main(mainURL, mainXPath, paraXPath, fileName, queryLi):
    with open(fileName,'w') as scrapeFile:
        nameLi = []
        liLinks = []
        htmlLi = []
        header = {'User-Agent': 'Mozilla/Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
##  Loop through the search queries
        for q in queryLi:
            increment = 0
##  Loop through 10 pages of Google News
            while increment < 11:
                url = mainURL + q
                if increment == 0:
                    mainRequest = requests.get(url, headers=header)
                else:
                    url = url + "&start=" + str(increment * 100)
                    mainRequest = requests.get(url, headers=header)
                if mainRequest.status_code != requests.codes.ok:
                    break
                else:
                    mainContent = html.fromstring(mainRequest.content)
                    writeToLog("Gathering links from URL: " + url + "\n")
                    liIncrementLinks = gatherLinks(mainContent, mainXPath)
##  Break pager loop if no links were found. These either suggests that the date is no longer current on the articles or the search string produced no articles
                    if len(liIncrementLinks) == 0:
                        break
                    liLinks.extend(liIncrementLinks)
##  Sleep for 7 seconds in between Google News pages
                    time.sleep(7)
                    fakeRequest = requests.get("http://www.bing.com")
                    increment = increment + 1
            if mainRequest.status_code != requests.codes.ok:
                writeToLog(url + " has status code of: " + str(mainRequest.status_code) + "\n")
                break
            else:
                htmlLi.extend(scrapeInfo(liLinks, paraXPath))
##  Sleep for 28 seconds in between search queries
            time.sleep(28)
##  If the list is empty don't go through the rest of the process
        if len(htmlLi) > 0:
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
    fileName = '/Scrapes/' + fileDate + '_CBCNews_Scrape.csv'
##  Declare list of search queries
    queryLi = ['money+laundering', 'lawsuit', 'scandal', 'fraud', 'illegal', 'criminal', 'crime', 'conviction', 'guilt', 'arrest', 'testify', 'corrupt', 'accused', 'kickback', 'investigate', 'investigation', 'bribe', 'grow-op', 'unethical', 'ponzi', 'terrorist', 'terrorism']
    mainURL = 'https://www.google.com/search?source=lnms&tbm=nws&tbs=qdr:w,sbd:1&num=100&q=site:www.cbc.ca/news+'
    mainXPath = '//*[@class="_cnc"]'
    paraXPath = '//p'
## If the NLTK packages are downloaded, run the main program
    if punktDL and aptDL:
        main(mainURL, mainXPath, paraXPath, fileName, queryLi)
    else:
        writeToLog('NLTK Punkt and Averaged_Perceptron_tagger need to be downloaded first.')
        writeToLog('Please sudo python and run nltk.download("punkt") and nltk.download("averaged_perceptron_tagger")')
##  Find total time in seconds of program run
    pName = os.path.basename(__file__)
    endTime = pyTimer.endTimer(startTime, pName)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
