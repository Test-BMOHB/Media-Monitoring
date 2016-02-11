from lxml import html
from lxml.etree import tostring
from datetime import datetime, timedelta
import requests, csv, re, time
##  Function to scrape info
def scrapeInfo(mainURL, mainContent, mainXPath, paraXPath):
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
        date = time.strptime(date, "%b %d, %Y")
        if currDate <= date:
            linkRequest = requests.get(link)
            linkContent = html.fromstring(linkRequest.content)
            linkXPath = linkContent.xpath(paraXPath)
            pageContent = ''
            for linkXElement in linkXPath:
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
                pageContent = pageContent + text
##  Adds list item
            li.append([pageContent,link])
    return li

##  Function to create the CSV file
def createCSV(liCSV, f1):
    writer = csv.writer(f1, delimiter=',')
##  Add a header row
    writer.writerow(["Content","Link"])
    for i in liCSV:
        rowStr = ''
        for e in i:
            rowStr = rowStr + '"' + str(e) + '"'
            rowStr = rowStr + ","
        rowStr = rowStr[:-1]
        print rowStr
        writer.writerow([rowStr])

##  Main Function
def main(mainURL, mainXPath, paraXPath, fileName):
    liData = []
    with open(fileName,'w') as scrapeFile:
        increment = 0
        while increment < 10:
## Set the request to seem like a browser to get correct layout of HTML
            header = {'User-Agent': 'Mozilla/Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            if increment == 0:
                mainRequest = requests.get(mainURL, headers=header)
            else:
                url = mainURL + "&start=" + str(increment * 10)
                mainRequest = requests.get(url, headers=header)
            mainContent = html.fromstring(mainRequest.content)
            liData.extend(scrapeInfo(mainURL, mainContent, mainXPath, paraXPath))
            increment = increment + 1
        createCSV(liData, scrapeFile)

##  Run main
main('https://www.google.ca/search?q=anti+money+laundering+and+money+laundering+and+arrested+and+convicted+and+sentenced&hl=en&gl=ca&authuser=0&tbm=nws&tbs=sbd:1', '//*[@class="g"]', '//p', 'GN_Scrape.csv')
