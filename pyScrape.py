from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time, traceback, sys
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
##  Moves past links that are not postings and add mainURL to links that need it
        if re.search("backpage.com/classifieds", link) is not None or re.search("backpage.com/adult/\?page=", link) is not None or re.search("backpage.com/adult", link) is not None or re.search("backpage.com/online", link) is not None or link.endswith('/') or link == 'http://www.backpage.com':
            continue
        elif re.search(mainURL, link) is None:
            link = url + link
            if link.count('/') < 3 or link.count('http') != 1:
                continue
        phoneNumber = []
        emailAddress = []
        websiteLink = []
        try:
            linkRequest = requests.get(link)
        except:
            writeToLog(link + " did not send back a response.\n")
            continue
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
                    number = number.replace(':','')
                    number = number.replace(';','')
                    number = number.replace(']','')
                    number = number.replace('/','')
                    number = number.replace('_','')                    
                    if len(number) == 10 or len(number) == 11:
                        phoneNumber.append(number)
##  Only grabs HTML 'a' tags
            for s in linkXElement.findall('.//a'):
                s = s.get('href')
                if s is not None:
                    if 'mailto:' in s:
                        s = s[7:]
                        emailAddress.append(s)
                    elif 'http' in s:
                        websiteLink.append(s)
##  Makes link into tinyURL
##        link = make_tinyURL(link)
##  Adds list item
        li.append([phoneNumber,emailAddress,websiteLink,[link]])
    return li

##  Function to return if a list contains a number
def is_number(st):
    for s in st:
        return s.isdigit()

##  Function to write to the CSV file
def writeToCSV(liCSV, writer):
    for i in liCSV:
        rowStr = ''
        num = []
        site = []
        write = True
        for n in i:
            if isinstance(n, list):
                if len(n) > 1:
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
        rowStr = rowStr[:-1]
        if rowStr.count(',') > 3:
            startHTTP = rowStr.index('http')
            httpStr = rowStr[startHTTP:]
            endHTTP = httpStr.index(',http')
            httpStr = httpStr[:endHTTP]
            start2HTTP = rowStr.index(httpStr)
            httpStr = '"' + httpStr + '"'
            rowStr = rowStr[:startHTTP] + httpStr + rowStr[(start2HTTP + len(httpStr)-2):]
        if write:
            writer.writerow([rowStr])
        else:
            num = list(set(num))
            site = list(set(site))
            rowCopy = rowStr
            for e in num:
                li = [e]
                rowStr = ''.join(li) + rowCopy
                rowCopy2 = rowStr
                for s in site:
                    s = '"' + s + '"'
                    lis = [s]
                    r = rowCopy2.split(',')
                    rowStr = r[0] + ',' + ''.join(lis) + ',' + r[2] + ',' + r[3]
                    writer.writerow([rowStr])
                if len(site) == 0:
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
    endStr = "It took " + str(tot) + " seconds to complete scrape of: "
    return endStr

##  Make tiny URL to hide actual URL from url
def make_tinyURL(url):
    request_url = ('http://tinyurl.com/api-create.php?url=' + url)
    try:
        response = requests.get(request_url)
    except:
        writeToLog('tinyURL did not respond with url for: ' + str(url) + '\n')
        return url
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
def main(mainURLList):
    startTime = time.time()
    currDate = datetime.now()
##  Make currDate Yesterday's date
    currDate = currDate - timedelta(days=1)
    currDate = currDate.strftime('%Y-%m-%d')
##  Increment through 999 possible pages
    writeToLog("*************************** " + currDate + " ***************************\n")
    with open('/var/www/html/ScreenScrape.csv','w') as scrapeFile:
        writer = csv.writer(scrapeFile, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
##  Add a header row
        writer.writerow(["PhoneNumber","Email_Address","Website","BackPage_Link"])
        try:
            for mainURL in mainURLList:
                liData = []
                writeToLog("\nMain scrape of: " + mainURL + "\n")
                startT = startTimer()
                startPage = 0
                endPage = 0
                increment = 1
                while increment < 1000:
##  If increment > 1 then add the page string to the URL
                    if increment == 1:
                        mainRequest = requests.get(mainURL + "adult/")
                    else:
                        mainRequest = requests.get(mainURL + "adult/?page=" + str(increment))
                    mainContent = html.fromstring(mainRequest.content)
                    date = mainContent.xpath('//*[@class="date"]')
                    dateStr = ''
##  Loop through dates on the page to make sure that the current date is on the page
                    for dateStr in date:
                        dateStr = tostring(dateStr)
                        dateStr = re.search("\w{3}. \w{3}. \d{1,2}", dateStr)
                        dateStr = datetime.strptime(dateStr.group(), '%a. %b. %d').date()
                        dateStr = dateStr.replace(year=datetime.now().year)
                        dateStr = dateStr.strftime('%Y-%m-%d')
                        if dateStr == currDate:
                            break
##  Compare current date to date on webpage
                    if dateStr == currDate:
                        if startPage == 0:
                            startPage = increment
                        liData.extend(scrapeInfo(mainURL, mainContent, '/html/body/div//*[@href]'))
##  Extend liData to include anything from the sponsorBoxContent xPath
                        liData.extend(scrapeInfo(mainURL, mainContent, '//*[@class="sponsorBoxContent"]/a'))
                    elif currDate < dateStr and currDate <> '':
                        increment = increment + 1
                        continue
                    else:
                        endPage = increment
                        writeToLog("Scraped pages: " + str(startPage) + " to " + str(endPage) + "\n")
                        writeToLog("Remove dups from scrape of: " + mainURL + "\n")
                        beforeDedup = len(liData)
                        liData = removeDuplicates(liData)
                        writeToLog(str(len(liData)) + " records of " + str(beforeDedup) + " left after deduplication\n")
                        break
                    increment = increment + 1
                writeToLog(endTimer(startT) + mainURL + "\n")
                writeToLog("Write to scrape to CSV\n")
                writeToCSV(liData, writer)
##  Sleep for 30 seconds and then request a different page to make it seem like a human is doing the surfing
                time.sleep(30)
                requests.get("http://www.google.com")
            endTime = time.time()
            totTime = endTime - startTime
            totTime = ("{0:.1f}".format(round(totTime,2)))
            writeToLog("It took " + str(totTime) + " seconds to scrape yesterday's postings.\n")
        except:
            e = traceback.format_exc()
            writeToLog("Unexpected error:" + str(e) + "\n")

##  List of all Canadian BP links and US links
mainURLList = ["http://alberta.backpage.com/", "http://britishcolumbia.backpage.com/", "http://manitoba.backpage.com/", "http://newbrunswick.backpage.com/", "http://stjohns.backpage.com/", "http://yellowknife.backpage.com/", "http://halifax.backpage.com/", "http://ontario.backpage.com/", "http://quebec.backpage.com/", "http://saskatchewan.backpage.com/", "http://whitehorse.backpage.com/", "http://alabama.backpage.com/", "http://alaska.backpage.com/", "http://arizona.backpage.com/", "http://arkansas.backpage.com/", "http://california.backpage.com/", "http://colorado.backpage.com/", "http://connecticut.backpage.com/", "http://delaware.backpage.com/", "http://florida.backpage.com/", "http://georgia.backpage.com/", "http://hawaii.backpage.com/", "http://idaho.backpage.com/", "http://illinois.backpage.com/", "http://indiana.backpage.com/", "http://iowa.backpage.com/", "http://kansas.backpage.com/", "http://kentucky.backpage.com/", "http://louisiana.backpage.com/", "http://maine.backpage.com/", "http://maryland.backpage.com/", "http://massachusetts.backpage.com/", "http://michigan.backpage.com/", "http://minnesota.backpage.com/", "http://mississippi.backpage.com/", "http://missouri.backpage.com/", "http://montana.backpage.com/", "http://nebraska.backpage.com/", "http://nevada.backpage.com/", "http://newhampshire.backpage.com/", "http://newjersey.backpage.com/", "http://newmexico.backpage.com/", "http://newyork.backpage.com/", "http://northcarolina.backpage.com/", "http://northdakota.backpage.com/", "http://ohio.backpage.com/", "http://oklahoma.backpage.com/", "http://oregon.backpage.com/", "http://pennsylvania.backpage.com/", "http://rhodeisland.backpage.com/", "http://southcarolina.backpage.com/", "http://southdakota.backpage.com/", "http://tennessee.backpage.com/", "http://texas.backpage.com/", "http://utah.backpage.com/", "http://vermont.backpage.com/", "http://virginia.backpage.com/", "http://washington.backpage.com/", "http://washingtondc.backpage.com/", "http://westvirginia.backpage.com/", "http://wisconsin.backpage.com/", "http://wyoming.backpage.com/"]
main(mainURLList)
