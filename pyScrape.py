from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time
##  Function to scrape info
def scrapeInfo(mainURL, mainContent, xPath):
    li = []
    mainLinksXPath = mainContent.xpath(xPath)
    mainLinksXPath = list(set(mainLinksXPath))
    for mainLinksElements in mainLinksXPath:
##  Only grabs the href of the 'a' tag
        link = mainLinksElements.get('href')
##  Takes '/' off end of mainURL
        url = mainURL[:-1]
        if re.search(url, link) is None:
            link = url + link
##  Moves past pages that have are not postings
        if re.search("https://my.backpage.com/classifieds", link) is not None or re.search("http://toronto.backpage.com/adult/?page=", link) is not None or re.search("http://my.backpage.com/classifieds", link) is not None or re.search(mainURL, link) is None:
            continue
        phoneNumber = []
        emailAddress = []
        websiteLink = []
        linkRequest = requests.get(link)
        linkContent = html.fromstring(linkRequest.content)
##  Only grabs HTML tags with class = "postingBody"
        linkXPath = linkContent.xpath('//*[@class="postingBody"]')
        for linkXElement in linkXPath:
            phoneNumber = []
            text = tostring(linkXElement)
##  Take out small icons in text
            icons = re.findall(r'&#\d*;', text)
            icons = list(set(icons))
            for icon in icons:
                text = re.sub(icon, '', text)
##  Take out HTML tags
            tags = re.findall('<[^>]+>', text)
            tags = list(set(tags))
            for tag in tags:
                text = text.replace(tag, '')
##  Take out whitespace
            text = re.sub('\s*', '', text)
##  Make numbers from words
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
##  11 digit regex
            phonenumbers = re.findall(r'1\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{4}|1[-]\d{3}[-]\d{3}[-]\d{4}|1[-]\d{3}[-]\d{7}|1[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d|1\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d',text)
##  10 digit regex
            if not phonenumbers:
                phonenumbers = re.findall(r'\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{4}|\d{3}[-]\d{3}[-]\d{4}|\d{3}[-]\d{7}|\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d|\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d',text)
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
                    if len(number) == 10 or len(number) == 11:
                        phoneNumber.append(number)
##  Only grabs HTML 'a' tags
            for s in linkXElement.findall('.//a'):
                s = s.get('href')
                if s is not None:
                    if 'mailto:' in s:
                        s = s[8:]
                        emailAddress.append(s)
                    elif 'http' in s:
                        websiteLink.append(s)
##  Adds list item
        link = make_tinyURL(link)
        li.append([phoneNumber,emailAddress,websiteLink,[link]])
    return li

##  Function to create the CSV file
def createCSV(liCSV, f1):
    writer = csv.writer(f1, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
##  Add a header row
    writer.writerow(["PhoneNumber","Email_Address","Website","BackPage_Link"])
    for i in liCSV:
        rowStr = ''
        num = []
        write = True
        for n in i:
            if isinstance(n, list):
                if len(n) > 1:
                    num = n
                    write = False
                else:
                    rowStr = rowStr + ''.join(n)
            else:
                rowStr = rowStr + n
            rowStr = rowStr + ","
        rowStr = rowStr[:-1]
        if write:
            writer.writerow([rowStr])
        else:
            num = list(set(num))
            rowCopy = rowStr
            for e in num:
                li = [e]
                rowStr = ''.join(li) + rowCopy
                writer.writerow([rowStr])

##  Start timer
def startTimer():
    start = time.time()
    return start

##  End timer
def endTimer(st):
    end = time.time()
    tot = end - st
    tot = ("{0:.1f}".format(round(tot,2)))
    endStr = "It took " + str(tot) + " seconds to complete process."
    return endStr

##  Make tiny URL to hide actual URL from url
def make_tinyURL(url):
    request_url = ('http://tinyurl.com/api-create.php?url=' + url)
    response = requests.get(request_url)
    content = html.fromstring(response.content)
    return content.text

##  Function to remove exact duplicate list entries
def removeDuplicates(dedup):
    finalList = []
    for x in dedup:
        if x not in finalList:
            finalList.append(x)
    return finalList

##  Write to log
def writeToLog(text):
    logFile = open('/var/www/html/pylog.txt','a')
    logFile.write(text)
    logFile.close()

##  Main Function
def main(mainURL):
    startTime = time.time()
    currDate = datetime.now()
##  Make currDate Yesterday's date
    currDate = currDate - timedelta(days=1)
    currDate = currDate.strftime('%Y-%m-%d')
    liData = []
    increment = 1
##  Increment through 999 possible pages
    writeToLog("*************************** " + currDate + " ***************************\n")
    with open('/var/www/html/ScreenScrape.csv','w') as scrapeFile:
        try:
            writeToLog("Main Scrape\n")
            while increment < 1000:
                writeToLog("Page: " + str(increment) + "\n")
                if increment == 1:
                    mainRequest = requests.get(mainURL + "adult/")
                else:
                    mainRequest = requests.get(mainURL + "adult/?page=" + str(increment))
                mainContent = html.fromstring(mainRequest.content)
                date = mainContent.xpath('//*[@class="date"]')
                for dateStr in date:
                    dateStr = tostring(dateStr)
                    dateStr = re.search("\w{3}. \w{3}. \d{1,2}", dateStr)
                    dateStr = datetime.strptime(dateStr.group(), '%a. %b. %d').date()
                    dateStr = dateStr.replace(year=datetime.now().year)
                    dateStr = dateStr.strftime('%Y-%m-%d')
##  Compare current date to date on webpage
                if dateStr == currDate:
                    startT = startTimer()
                    liData.extend(scrapeInfo(mainURL, mainContent, '/html/body/div//*[@href]'))
##  Extend liData to include anything from the sponsorBoxContent xPath
                    liData.extend(scrapeInfo(mainURL, mainContent, '//*[@class="sponsorBoxContent"]/a'))
                    writeToLog(endTimer(startT) + "\n")
                elif currDate < dateStr and currDate <> '':
                    increment = increment + 1
                    continue
                else:
                    startT = startTimer()
                    writeToLog("Remove Dups from Scrape\n")
                    writeToLog(len(liData) + " records from scrape\n")
                    liData = removeDuplicates(liData)
                    writeToLog(len(liData) + " records after deduplication\n")
                    writeToLog(endTimer(startT) + "\n")
                    startT = startTimer()
                    writeToLog("Create CSV for Scrape\n")
                    createCSV(liData, scrapeFile)
                    writeToLog(endTimer(startT) + "\n")
                    endTime = time.time()
                    totTime = endTime - startTime
                    totTime = ("{0:.1f}".format(round(totTime,2)))
                    writeToLog("It took " + str(totTime) + " seconds to scrape yesterday's pages.\n")
                    logFile.close()
##                    exit()
                increment = increment + 1
        except:
            writeToLog("Unexpected error:" + sys.exc_info()[0] + "\n")
            logFile.close()

mainURL = "http://toronto.backpage.com/"
main(mainURL)
