from lxml import html
from lxml.etree import tostring
from functools import partial
from datetime import datetime, timedelta
import requests, csv, re, time, traceback, sys
##  Function to scrape info
def scrapeInfo(mainURL, mainContent, xPath):
    li = []
    mainLinksXPath = mainContent.xpath(xPath)
    mainLinksXPath = list(set(mainLinksXPath))
    for mainLinksElements in mainLinksXPath:
        link = mainLinksElements.get('href')
        if re.search(mainURL, link) is None:
            link = mainURL + link
            if link.count('/') < 3 or link.count('http') != 1:
                continue
        phoneNumber = []
        emailAddress = []
        websiteLink = []
        try:
            linkRequest = requests.get(link)
        except:
            continue
        linkContent = html.fromstring(linkRequest.content)
        linkXPath = linkContent.xpath('//*[@class="showcontact"]')
        if len(linkXPath) > 0:
            for showContact in linkXPath:
                contactLink = showContact.get('href')
                contactLink = mainURL + contactLink
                print contactLink
                try:
                    linkRequest = requests.get(link)
                except:
                    continue
                contactContent = html.fromstring(linkRequest.content)
                phoneNumber = []
                text = tostring(contactContent)
                icons = re.findall(r'&#\d*;', text)
                icons = list(set(icons))
                for icon in icons:
                    text = re.sub(icon, '', text)
                tags = re.findall('<[^>]+>', text)
                tags = list(set(tags))
                for tag in tags:
                    text = text.replace(tag, '')
                text = re.sub('\s*', '', text)
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
                phonenumbers = re.findall(r'1\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{4}|1[-]\d{3}[-]\d{3}[-]\d{4}|1[-]\d{3}[-]\d{7}|1[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d[.]*\d|1\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d[-]*\d',text)
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
        li.append([phoneNumber,[link]])
    return li

##  Function to return if a list contains a number
def is_number(st):
    for s in st:
        return s.isdigit()

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

##  Function to remove exact duplicate list entries
def removeDuplicates(dedup):
    finalList = []
    for x in dedup:
        if x not in finalList:
            finalList.append(x)
    return finalList

##  Write to log
def writeToLog(text):
    logFile = open('/var/www/html/pyCLlog.txt','a')
    logFile.write(text)
    logFile.close()

##  Main Function
def main(mainURLList, category):
    startTime = time.time()
    currDate = datetime.now()
##  Make currDate Yesterday's date
    currDate = currDate - timedelta(days=1)
    currDate = currDate.strftime('%Y-%m-%d')
##  Increment through 999 possible pages
    writeToLog("*************************** " + currDate + " ***************************\n")
    try:
        for mainURL in mainURLList:
            mainURL = ''.join(mainURL)
            liData = []
            writeToLog("\nMain scrape of: " + mainURL + "\n")
            startT = startTimer()
            increment = 0
            urlRequest = "http:" + mainURL + "/search/" + str(category)
            while increment < 1000:
                if increment == 0:
                    mainRequest = requests.get(urlRequest)
                else:
                    urlRequest = "http:" + urlRequest + "?s=" + str(increment)
                    mainRequest = requests.get(urlRequest)
                dateStr = ''
                mainContent = html.fromstring(mainRequest.content)
                date = mainContent.xpath('//time')
                for dateStr in date:
                    dateStr = dateStr.get("datetime")
                    dateStr = dateStr[:-6]
                    if dateStr == currDate:
                        break
                if dateStr == currDate:
                    liData.extend(scrapeInfo(mainURL, mainContent, '//*[@class="hdrlnk"]'))
                else:
                    writeToLog("Remove dups from scrape of: " + mainURL + "\n")
                    beforeDedup = len(liData)
                    liData = removeDuplicates(liData)
                    writeToLog(str(len(liData)) + " records of " + str(beforeDedup) + " left after deduplication\n")
                    break
                increment = increment + 100
            writeToLog(endTimer(startT) + mainURL + "\n")
            time.sleep(30)
            requests.get("http://www.google.com")
        endTime = time.time()
        totTime = endTime - startTime
        totTime = ("{0:.1f}".format(round(totTime,2)))
        writeToLog("It took " + str(totTime) + " seconds to scrape yesterday's postings.\n")
    except:
        e = traceback.format_exc()
        writeToLog("Unexpected error:" + str(e) + "\n")

categories = ["cas","m4m","m4w","msr","w4w","w4m"]
sourceURL = "http://www.craigslist.org/about/sites#US"
mainURLList = []
sourceRequest = requests.get(sourceURL)
sourceContent = html.fromstring(sourceRequest.content)
sourceXPath = sourceContent.xpath('//a')
sourceXPath = list(set(sourceXPath))
for sourceElements in sourceXPath:
    link = sourceElements.get('href')
    if str(link)[:1] <> '#' and link is not None and re.search('www.craigslist.org',link) is None and re.search('forums.craigslist.org',link) is None:
        mainURLList.append([link])

with open('/var/www/html/CL_ScreenScrape.csv','w') as scrapeFile:
    writer = csv.writer(scrapeFile, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
    writer.writerow(["PhoneNumber","BackPage_Link"])
    func = partial(main, mainURLList)
    results = map(func, categories)
    final = results[0] + results[1] + results[2] + results[3] + results[4] + results[5]
    writeToLog("Write to scrape to CSV\n")
    for i in final:
        writer.writerow(i)
