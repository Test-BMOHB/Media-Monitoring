from lxml import html
from lxml.etree import tostring
import requests, csv, re, json
##  Function to scrape info
def scrapeInfo(mainURL, mainContent, mainXPath, paraXPath):
    li = []
    mainLinksXPath = mainContent.xpath(mainXPath)
    mainLinksXPath = list(set(mainLinksXPath))
    for mainLinksElements in mainLinksXPath:
        link = mainLinksElements.find('a')
        link = link.get('href')
        link = 'https://www.leafly.com' + link
        linkRequest = requests.get(link)
        linkContent = html.fromstring(linkRequest.content)
        linkXPath = linkContent.xpath(paraXPath)
        finList = []
        print "Scraping " + link
        for linkXElement in linkXPath:
            text = tostring(linkXElement)
            if 'setPreloadedResults' in text:
                text = text[(text.index('setPreloadedResults') + 21):]
                text = text[:(text.index('}]);') + 1)]
                strDict = ''
                openLi = False
                count = 0
                for t in text:
                    if t == '{':
                        openLi = True
                        count = count + 1
                    if openLi:
                        strDict = strDict + t
                    if t == '}':
                        count = count - 1
                        if count == 0:
                            openLi = False
                            d = json.loads(strDict)
                            finList.append(d)
                            strDict = ''
##  Adds list item
        for i in finList:
            name = ''.join(filter(None, [i["Name"]]))
            address = ' '.join(filter(None, [i["Address1"],i["Address2"]]))
            city = ''.join(filter(None, [i["City"]]))
            state = ''.join(filter(None, [i["State"]]))
            zipcode = ''.join(filter(None, [i["Zip"]]))
            url = "https:/www.leafly.com/dispensary-info/" + str(i["UrlName"])
            phone = ''.join(filter(None, [i["Phone"]]))
            phone = phone.replace('.','').replace('-','').replace('(','').replace(')','')
            phone = phone.replace('A','2').replace('B','2').replace('C','2')
            phone = phone.replace('D','3').replace('E','3').replace('F','3')
            phone = phone.replace('G','4').replace('H','4').replace('I','4')
            phone = phone.replace('J','5').replace('K','5').replace('L','5')
            phone = phone.replace('M','6').replace('N','6').replace('O','6')
            phone = phone.replace('P','7').replace('Q','7').replace('R','7').replace('S','7')
            phone = phone.replace('T','8').replace('U','8').replace('V','8')
            phone = phone.replace('W','9').replace('X','9').replace('Y','9').replace('Z','9')
            phones = []
            if len(phone) > 11:
                phones = phone.split(' ')
                for p in phones:
                    if len(p) > 6:
                        p = p.replace(' ', '')
                        li.append([name,p,address,city,state,zipcode,url,link])
            else:
                phone = phone.replace(' ', '')
                li.append([name,phone,address,city,state,zipcode,url,link])
    return li

##  Function to remove exact duplicate list entries
def removeDuplicates(dedup):
    print len(dedup)
    finalList = []
    for x in dedup:
        if x not in finalList:
            finalList.append(x)
    print len(finalList)
    return finalList

##  Function to create the CSV file
def createCSV(liCSV, f1):
    print "Writing to CSV"
    writer = csv.writer(f1, delimiter='^')
##  Add a header row
    writer.writerow(["Company","PhoneNumber","Address","City","State","ZipCode","Website","Link"])
    for i in liCSV:
        rowStr = ''
        for e in i:
            rowStr = rowStr + str(e)
            rowStr = rowStr + '^'
        rowStr = rowStr[:-1]
        writer.writerow([rowStr])

##  Main Function
def main(mainURL, mainXPath, linkXPath, fileName):
    liData = []
    with open(fileName,'w') as scrapeFile:
        mainRequest = requests.get(mainURL)
        mainContent = html.fromstring(mainRequest.content)
        liData.extend(scrapeInfo(mainURL, mainContent, mainXPath, linkXPath))
        liData = removeDuplicates(liData)
        createCSV(liData, scrapeFile)

##  Run main
main('https://www.leafly.com/finder', '//*[@class="col-xs-6 col-md-4 spacer-bottom-xs"]', './/script', 'Leafly_Scrape.csv')
