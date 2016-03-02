##*********************HEADER*********************##
##Developer         : Justin Suelflow
##Date              : 2/25/2016
##Program Name      : pyScrape_Backpage
##Description       : Loop through all Backpage.com adult postings to find phone number, email,
##                    URL of personal website, and URL of Backpage link
##Python Version    : 2.7.11
##Prereqs Knowledge : Python, HTML, CSS, XPath
##Prereqs Hardware  : Any computer that has a C++ compiler (libxml2 uses C++)
##Prereqs Software  : Python, pip
##Python Libraries  : LXML, requests, csv, json, re, libxml2, libxslt
##Python file       : pyTimer.py file needs to be in same directory as pyScrape.py
##Static variables  : '/var/www/html/pylog_Backpage.txt', '/var/www/html/ScreenScrape.csv', "adult/?page=",
##                      regex for finding phone numbers, header row, all xpath, and mainURLList
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       02/25/2016    Justin Suelflow   Tested version of production code
##    2       02/25/2016    Justin Suelflow   Added comments to code
##    3       02/29/2016    Justin Suelflow   Deleted timer functions to import timer python file pyTimer
##    4       03/01/2016    Justin Suelflow   Standardized comments, added proper main function call, and
##                                              renamed file to pyScrape_Backpage.py to standardize file naming
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
##  pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time, traceback, sys, pyTimer
##*********************END IMPORT*********************##

##*********************FUNCTIONS*********************##
##  Function: scrapeInfo
##  Description: Scrapes phoneNumber, emailAddress and websiteLink from mainURL
##  Parameters: mainURL = string type, mainContent = string type, xPath = string type
##  Returns: list
def scrapeInfo(mainURL, mainContent, xPath):
    li = []
    mainLinksXPath = mainContent.xpath(xPath)
##  Creates a set of mainLinksXPath which takes out the duplicates and then format the set back to a list
    mainLinksXPath = list(set(mainLinksXPath))
##  Loop through elements in mainLinksXPath
    for mainLinksElements in mainLinksXPath:
##  Get the href parameter from the xpath elements
        link = mainLinksElements.get('href')
##  Takes '/' off end of mainURL
        url = mainURL[:-1]
##  Skips the links that are not postings and add mainURL to links that need it
        if re.search("backpage.com/classifieds", link) is not None or re.search("backpage.com/adult/\?page=", link) is not None or re.search("backpage.com/adult", link) is not None or re.search("backpage.com/online", link) is not None or link.endswith('/') or link == 'http://www.backpage.com':
            continue
        elif re.search(mainURL, link) is None:
            link = url + link
##  If the link is not a proper url to request, continue to next element
            if link.count('/') < 3 or link.count('http') != 1:
                continue
        phoneNumber = []
        emailAddress = []
        websiteLink = []
##  Send a http request to the link
        try:
            linkRequest = requests.get(link)
        except:
##  If request does not send a response, write the link to the log and continue to next link
            writeToLog(link + " did not send back a response.\n")
            continue
##  Translate the content from the request to HTML
        linkContent = html.fromstring(linkRequest.content)
##  Use xpath to only grab HTML tags with the CSS class "postingBody"
        linkXPath = linkContent.xpath('//*[@class="postingBody"]')
##  Loop through elements in linkXPath
        for linkXElement in linkXPath:
            phoneNumber = []
            text = tostring(linkXElement)
##  Create a list of small icons and emojis in the text
            icons = re.findall(r'&#\d*;', text)
##  Deduplicate the list of icons
            icons = list(set(icons))
##  Loop through all of the icons to take them out of the text
            for icon in icons:
                text = re.sub(icon, '', text)
##  Create a list of HTML tags in the text
            tags = re.findall('<[^>]+>', text)
##  Deduplicate the list of HTML tags
            tags = list(set(tags))
##  Loop through all of the HTML tags to take them out of the text
            for tag in tags:
                text = text.replace(tag, '')
##  Take out whitespace
            text = re.sub('\s*', '', text)
##  Replace the text where a number is spelled out to a digit
            numReplace = re.compile(re.escape('zero'), re.IGNORECASE)
            text = numReplace.sub('0', text)
            numReplace = re.compile(re.escape('one'), re.IGNORECASE)
            text = numReplace.sub('1', text)
            numReplace = re.compile(re.escape('two'), re.IGNORECASE)
            text = numReplace.sub('2', text)
            numReplace = re.compile(re.escape('three'), re.IGNORECASE)
            text = numReplace.sub('3', text)
            numReplace = re.compile(re.escape('four'), re.IGNORECASE)
            text = numReplace.sub('4', text)
            numReplace = re.compile(re.escape('five'), re.IGNORECASE)
            text = numReplace.sub('5', text)
            numReplace = re.compile(re.escape('six'), re.IGNORECASE)
            text = numReplace.sub('6', text)
            numReplace = re.compile(re.escape('seven'), re.IGNORECASE)
            text = numReplace.sub('7', text)
            numReplace = re.compile(re.escape('eight'), re.IGNORECASE)
            text = numReplace.sub('8', text)
            numReplace = re.compile(re.escape('nine'), re.IGNORECASE)
            text = numReplace.sub('9', text)
            numReplace = re.compile(re.escape('ten'), re.IGNORECASE)
            text = numReplace.sub('10', text)
            numReplace = re.compile(re.escape('twenty'), re.IGNORECASE)
            text = numReplace.sub('20', text)
            numReplace = re.compile(re.escape('thirty'), re.IGNORECASE)
            text = numReplace.sub('30', text)
            numReplace = re.compile(re.escape('fourty'), re.IGNORECASE)
            text = numReplace.sub('40', text)
            numReplace = re.compile(re.escape('fifty'), re.IGNORECASE)
            text = numReplace.sub('50', text)
            numReplace = re.compile(re.escape('sixty'), re.IGNORECASE)
            text = numReplace.sub('60', text)
            numReplace = re.compile(re.escape('seventy'), re.IGNORECASE)
            text = numReplace.sub('70', text)
            numReplace = re.compile(re.escape('eighty'), re.IGNORECASE)
            text = numReplace.sub('80', text)
            numReplace = re.compile(re.escape('ninety'), re.IGNORECASE)
            text = numReplace.sub('90', text)
##  Finds phone numbers in the text within the HTML
##  11 digit regex to look for several different variations of phone number combinations
            phonenumbers = re.findall(r'1\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{4}|1[-]\d{3}[-]\d{3}[-]\d{4}|1[-]\d{3}[-]\d{7}|1[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d|1\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d',text)
##  If the 11 digit regex did not find a phone number, look for a 10 digit number
##  10 digit regex to look for several different variations of phone number combinations
            if not phonenumbers:
                phonenumbers = re.findall(r'\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{4}|\d{3}[-]\d{3}[-]\d{4}|\d{3}[-]\d{7}|\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d|\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d',text)
##  If a phone number is found, loop through the list and replace all special characters with blanks
            if phonenumbers:
                for number in phonenumbers:
                    number = number.replace(' ','')
                    number = number.replace('(','')
                    number = number.replace(')','')
                    number = number.replace('-','')
                    number = number.replace('.','')
                    number = number.replace('*','')
                    number = number.replace('~','')
                    number = number.replace(',','')
                    number = number.replace(':','')
                    number = number.replace(';','')
                    number = number.replace(']','')
                    number = number.replace('/','')
                    number = number.replace('_','')
##  If phone number is 10 or 11 digits, add to list
                    if len(number) == 10 or len(number) == 11:
                        phoneNumber.append(number)
##  Only find HTML anchor tags and loop through elements
            for s in linkXElement.findall('.//a'):
##  Get the href parameter from the anchor tags
                s = s.get('href')
##  If the element has a 'href', check for 'mailto:' or 'http'
                if s is not None:
                    if 'mailto:' in s:
##  If 'mailto:' is found in element, delete 'mailto:' and add element to emailAddress list
                        s = s[7:]
                        emailAddress.append(s)
                    elif 'http' in s:
##  If 'http' is found in element, delete 'http' and add element to websiteLink list
                        websiteLink.append(s)
##  tinyURL is commented out because it extends runtime significantly
##  Makes link into tinyURL
##        link = make_tinyURL(link)
##  Adds list item
        li.append([phoneNumber,emailAddress,websiteLink,[link]])
    return li

##  Function: is_number
##  Description: Return if a list contains a digit
##  Parameters: st = list type
##  Returns: True or False
def is_number(st):
    for s in st:
        return s.isdigit()

##  Function	: writeToCSV
##  Description	: Writes list to a CSV file
##  Parameters	: liCSV = list type, writer = csv.writer type
##  Returns	:
def writeToCSV(liCSV, writer):
##  Loop through all elements in the list
    for i in liCSV:
        rowStr = ''
        num = []
        site = []
        write = True
##  Some elements are lists so it is needed to loop through each element again
        for n in i:
##  If the element is a list, check if the length of the list is greater than 1
            if isinstance(n, list):
                if len(n) > 1:
##  If the list length is greater than 1, check if the element is a number
                    if is_number(n):
                        num = n
                    else:
                        site = n
                    write = False
                else:
                    rowStr = rowStr + ''.join(n)
            else:
                rowStr = rowStr + n
            rowStr = rowStr + ","
##  Take the last ',' off of the rowStr to finish the row
        rowStr = rowStr[:-1]
##  If rowStr has more than 3 commas, there is an additional http link that needs to be quoted
        if rowStr.count(',') > 3:
##  Finds index of first http link
            startHTTP = rowStr.index('http')
            httpStr = rowStr[startHTTP:]
##  Finds index of the end of first http link
            endHTTP = httpStr.index(',http')
            httpStr = httpStr[:endHTTP]
##  Find index of second http link
            start2HTTP = rowStr.index(httpStr)
##  Quotes first http link
            httpStr = '"' + httpStr + '"'
##  Adds the quoted first http link to the second link that is already quoted
            rowStr = rowStr[:startHTTP] + httpStr + rowStr[(start2HTTP + len(httpStr)-2):]
##  If the list from above only has 1 number, write the row to the CSV file
        if write:
            writer.writerow([rowStr.encode('utf-8')])
        else:
##  Take out duplicate phone numbers and websites
            num = list(set(num))
            site = list(set(site))
            rowCopy = rowStr
##  Loop through all phone numbers in list
            for e in num:
                li = [e]
                rowStr = ''.join(li) + rowCopy
                rowCopy2 = rowStr
##  Loop through all websites in list to quote them and join them together on each CSV entry
                for s in site:
                    s = '"' + s + '"'
                    lis = [s]
                    r = rowCopy2.split(',')
                    rowStr = r[0] + ',' + ''.join(lis) + ',' + r[2] + ',' + r[3]
                    writer.writerow([rowStr.encode('utf-8')])
                if len(site) == 0:
                    writer.writerow([rowStr.encode('utf-8')])

##  tinyURL function is commented out because it is not used for runtime considerations
##  Function saved if needed to hide the URL links of the postings
##  Used in scrapeInfo function
##  Function: make_tinyURL
##  Description: Make tiny URL to hide actual URL from url
##  Parameters: url = string type
##  Returns: string
##def make_tinyURL(url):
##    request_url = ('http://tinyurl.com/api-create.php?url=' + url)
##    try:
##        response = requests.get(request_url)
##    except:
##        writeToLog('tinyURL did not respond with url for: ' + str(url) + '\n')
##        return url
##    content = html.fromstring(response.content)
##    return content.text

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
    logFile = open('/var/www/html/pylog_Backpage.txt','a')
    logFile.write(text)
##  Close log file
    logFile.close()

##*********************MAIN FUNCTION*********************##
##  Function	: main
##  Description	: Loops through all URLs, starts timers, call other functions, and increments through pages
##  Parameters	: mainURLList = list type
##  Returns	:
def main(mainURLList):
    currDate = datetime.now()
##  Make currDate Yesterday's date
    currDate = currDate - timedelta(days=1)
    currDate = currDate.strftime('%Y-%m-%d')
    writeToLog("*************************** " + currDate + " ***************************\n")
##  Open a file and overwrite the existing file or create a new file if needed
    with open('/var/www/html/ScreenScrape.csv','w') as scrapeFile:
        writer = csv.writer(scrapeFile, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
##  Add a header row
        writer.writerow(["PhoneNumber","Email_Address","Website","BackPage_Link"])
        try:
##  Loop through all urls in the mainURLList
            for mainURL in mainURLList:
                liData = []
                writeToLog("\nMain scrape of: " + mainURL + "\n")
                startT = pyTimer.startTimer()
                startPage = 0
                endPage = 0
                increment = 1
##  Increment through 999 possible pages
                while increment < 1000:
##  If increment > 1 then add the page string to the URL
##  Http request the mainURL
                    if increment == 1:
                        mainRequest = requests.get(mainURL + "adult/")
                    else:
                        mainRequest = requests.get(mainURL + "adult/?page=" + str(increment))
##  Translate the request content to HTML
                    mainContent = html.fromstring(mainRequest.content)
##  Use xpath to only grab HTML tags with the CSS class "date"
                    date = mainContent.xpath('//*[@class="date"]')
                    dateStr = ''
##  Loop through dates on the page to make sure that the current date is on the page
                    for dateStr in date:
                        dateStr = tostring(dateStr)
                        dateStr = re.search("\w{3}. \w{3}. \d{1,2}", dateStr)
			dateStr = dateStr.group() + " - " + str(datetime.now().year)
                        dateStr = datetime.strptime(dateStr, '%a. %b. %d - %Y').date()
                        dateStr = dateStr.strftime('%Y-%m-%d')
                        if dateStr == currDate:
                            break
##  Compare current date to date on webpage
                    if dateStr == currDate:
                        if startPage == 0:
                            startPage = increment
##  Extend liData to include anything from the main body of the postings
                        liData.extend(scrapeInfo(mainURL, mainContent, '/html/body/div//*[@href]'))
##  Extend liData to include anything from the sponsorBoxContent
                        liData.extend(scrapeInfo(mainURL, mainContent, '//*[@class="sponsorBoxContent"]/a'))
##  If the date on the page is greater than the currDate variable or the currDate variable is blank, go to next page
                    elif currDate < dateStr and currDate <> '':
                        increment = increment + 1
                        continue
                    else:
                        endPage = increment
                        writeToLog("Scraped pages: " + str(startPage) + " to " + str(endPage) + "\n")
                        writeToLog("Remove dups from scrape of: " + mainURL + "\n")
                        beforeDedup = len(liData)
##  Call function removeDuplicates
                        liData = removeDuplicates(liData)
                        writeToLog(str(len(liData)) + " records of " + str(beforeDedup) + " left after deduplication\n")
                        break
                    increment = increment + 1
                writeToLog(pyTimer.endTimer(startT) + mainURL + "\n")
                writeToLog("Write to scrape to CSV\n")
##  Call createCSV function to write the list data to the scrapeFile
##  createCSV needs a list and a writer from the open file to run
                writeToCSV(liData, writer)
##  Sleep for 30 seconds and then request a different page to make it seem like a human is doing the surfing
                time.sleep(30)
                requests.get("http://www.google.com")
        except:
            e = traceback.format_exc()
            writeToLog("Unexpected error:" + str(e) + "\n")
##*********************END MAIN FUNCTION*********************##

##*********************END FUNCTIONS*********************##

##*********************PROGRAM*********************##
##  If statement makes this program standalone
##  Do not need this if statement if another program will be calling above functions
if __name__ == "__main__":
##  Create start time
    startTime = pyTimer.startTimer()
##  Create list of all Canadian Backpage links and US Backpage links to be used for main function
    mainURLList = ["http://alberta.backpage.com/", "http://britishcolumbia.backpage.com/", "http://manitoba.backpage.com/", "http://newbrunswick.backpage.com/", "http://stjohns.backpage.com/", "http://yellowknife.backpage.com/", "http://halifax.backpage.com/", "http://ontario.backpage.com/", "http://quebec.backpage.com/", "http://saskatchewan.backpage.com/", "http://whitehorse.backpage.com/", "http://alabama.backpage.com/", "http://alaska.backpage.com/", "http://arizona.backpage.com/", "http://arkansas.backpage.com/", "http://california.backpage.com/", "http://colorado.backpage.com/", "http://connecticut.backpage.com/", "http://delaware.backpage.com/", "http://florida.backpage.com/", "http://georgia.backpage.com/", "http://hawaii.backpage.com/", "http://idaho.backpage.com/", "http://illinois.backpage.com/", "http://indiana.backpage.com/", "http://iowa.backpage.com/", "http://kansas.backpage.com/", "http://kentucky.backpage.com/", "http://louisiana.backpage.com/", "http://maine.backpage.com/", "http://maryland.backpage.com/", "http://massachusetts.backpage.com/", "http://michigan.backpage.com/", "http://minnesota.backpage.com/", "http://mississippi.backpage.com/", "http://missouri.backpage.com/", "http://montana.backpage.com/", "http://nebraska.backpage.com/", "http://nevada.backpage.com/", "http://newhampshire.backpage.com/", "http://newjersey.backpage.com/", "http://newmexico.backpage.com/", "http://newyork.backpage.com/", "http://northcarolina.backpage.com/", "http://northdakota.backpage.com/", "http://ohio.backpage.com/", "http://oklahoma.backpage.com/", "http://oregon.backpage.com/", "http://pennsylvania.backpage.com/", "http://rhodeisland.backpage.com/", "http://southcarolina.backpage.com/", "http://southdakota.backpage.com/", "http://tennessee.backpage.com/", "http://texas.backpage.com/", "http://utah.backpage.com/", "http://vermont.backpage.com/", "http://virginia.backpage.com/", "http://washington.backpage.com/", "http://washingtondc.backpage.com/", "http://westvirginia.backpage.com/", "http://wisconsin.backpage.com/", "http://wyoming.backpage.com/"]
    main(mainURLList)
##  Find total time in seconds of program run
    endTime = pyTimer.endTimer(startTime)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
