##Developer     : Justin Suelflow
##Date          : 2/25/2016
##Program Name  : pyScrape_WeedMaps
##Version #     : 2
##Description   : Loop through all Weedmaps.com state and territory websites to find phone number, business name
##                  address, city, state, zip code, and url of weedmaps link
##Python Version: 2.7.10
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: Any computer that has a C++ compiler (libxml2 uses C++)
##Prereqs Software: Python, pip
##Python Libraries: LXML, requests, csv, json, re, libxml2, libxslt
##Static variables: 'wmVariables', './/a', '"listings":[{', user agent header,
##                  header row in CSV, mainURL, mainXPath, paraXPath
##-----------------------------------------------------------------------------
## History  | ddmmyyyy  |  User           |                Changes
##    1       25022016    Justin Suelflow   Tested version of production code
##    2       25022016    Justin Suelflow   Added comments to code
##-----------------------------------------------------------------------------
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
from lxml import html
from lxml.etree import tostring
import requests, csv, re, json
##  Function to scrape info
def scrapeInfo(mainURL, mainContent, mainXPath, paraXPath):
    li = []
    mainLinksXPath = mainContent.xpath(mainXPath)
##  Creates a set of mainLinksXPath which takes out the duplicates and then format the set back to a list
    mainLinksXPath = list(set(mainLinksXPath))
##  Loop through elements in mainLinksXPath
    for mainLinksElements in mainLinksXPath:
## Translate the element to a string and then formate to HTML
        h = tostring(mainLinksElements)
        h = html.fromstring(h)
##  Use xpath to get all anchor tags in HTML element
        x = h.xpath('.//a')
## Loop through each element in the xpath
## This will loop through all anchor tags
        for e in x:
##  Get the href parameter from the anchor tags
            link = e.get('href')
            link = 'https://weedmaps.com' + link
##  Send a http request to the link
            linkRequest = requests.get(link)
##  Translate the content from the request to HTML
            linkContent = html.fromstring(linkRequest.content)
##  Use xpath to find the elements in the HTML
            linkXPath = linkContent.xpath(paraXPath)
            finList = []
            print "Scraping " + link
##  Loop through elements in linkXPath
            for linkXElement in linkXPath:
                text = tostring(linkXElement)
##  If the xpath text has 'wmVariables' in the text, proceed
##  'wmVariables' is the distinguishing factor on WeedMaps to find the needed script tag                
                if 'wmVariables' in text:
                    try:
                        text = text[(text.index('"listings":[{')):]
                        text = text[:(text.index('}],'))]
                    except:
                        continue
                    strDict = ''
                    openLi = False
                    count = 0
##  Loop through all characters in the xpath text
##  This loop looks through the text to find the opening and closing brackets to create a proper dictionary
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
##  Need to use json.loads because the data is in JSON format; the entries are not all the same length
##  If the json.loads does not work because of a data error, continue to the next entry in the list
                                try:
                                    d = json.loads(strDict)
                                except:
                                    continue
                                finList.append(d)
                                strDict = ''
##  Loop through finList to translate elements and add to list
            for i in finList:
##  Filter will bypass all values that are None
##  Join concatenates the values if there are multiple
                try:
                    name = ''.join(filter(None, [i["name"]]))
                    address = ' '.join(filter(None, [i["address"]]))
                    city = ''.join(filter(None, [i["city"]]))
                    state = ''.join(filter(None, [i["state"]]))
                    zipcode = ''.join(filter(None, [i["zip_code"]]))
                    url = str(i["url"])
                    phone = ''.join(filter(None, [i["phone_number"]]))
##  Replace any letters in a phone number to digits
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
##  If the phone number is greater than 11 characters long, split the phone number on spaces to find multiple numbers
                    if len(phone) > 11:
                        phones = phone.split(' ')
##  Loop through the multiple numbers and add to the list if the number is greater than 6 characters long
                        for p in phones:
                            if len(p) > 6:
                                p = p.replace(' ', '')
                                li.append([name,p,address,city,state,zipcode,url])
##  If the phone number is 11 characters long or shorter, add to the list
                    else:
                        phone = phone.replace(' ', '')
                        li.append([name,phone,address,city,state,zipcode,url])
                except:
                    continue
    return li

##  Function to remove exact duplicate list entries
def removeDuplicates(dedup):
    print len(dedup)
    finalList = list(set(dedup))
##    finalList = []
##    for x in dedup:
##        if x not in finalList:
##            finalList.append(x)
    print len(finalList)
    return finalList

##  Function to create the CSV file
def createCSV(liCSV, f1):
    print "Writing to CSV"
##  Use the ^ as a delimiter because the data on WeedMaps has lots of other special characters including commas
##  Needed to find a special character that was not used by the data
    writer = csv.writer(f1, delimiter='^')
##  Add a header row to the CSV
    writer.writerow(["Company","PhoneNumber","Address","City","State","ZipCode","Website"])
##  Loop through all elements in the list
    for i in liCSV:
        rowStr = ''
##  Some elements are lists so it is needed to loop through each element again
        for e in i:
            rowStr = rowStr + e.encode('utf-8')
            rowStr = rowStr + '^'
##  Take the last ^ off of the rowStr to finish the row
        rowStr = rowStr[:-1]
##  Write the row to the CSV file
        writer.writerow([rowStr])

##  Main Function
def main(mainURL, mainXPath, linkXPath, fileName):
    liData = []
    print '***********************************************************************\n'
##  Open a file and overwrite the existing file or create a new file if needed
    with open(fileName,'w') as scrapeFile:
        for url in mainURL:
##  Set header variable to trick the http request to think a web browser is opening the page
            header = {'User-Agent': 'Mozilla/Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
##  Http request the mainURL with a header variable
            mainRequest = requests.get(url, headers=header)
##  Translate the request content to HTML
            mainContent = html.fromstring(mainRequest.content)
##  Add the information that comes from the scrapeInfo function to a list
##  scrapeInfo needs the url, content and 2 xpath variables to call the function
##  scrapeInfo returns a list when completed
            liData.extend(scrapeInfo(url, mainContent, mainXPath, linkXPath))
##  Call function removeDuplicates to print the length of the list before and after deduplication
        liData = removeDuplicates(liData)
##  Call createCSV function to write the list data to the scrapeFile
##  createCSV needs a list and an open file to run
        createCSV(liData, scrapeFile)

##  Run main
##  main needs a url, 2 xpaths and a filename to run
main(['https://weedmaps.com/dispensaries/in/united-states/','https://weedmaps.com/dispensaries/in/canada/'],  '//noscript', './/script','/var/www/html/Dispensaries_US_Scrape.csv')
