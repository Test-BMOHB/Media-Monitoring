##*********************HEADER*********************##
##Developer     : Justin Suelflow
##Date          : 03/01/2016
##Program Name  : pyScrape_PotLocator
##Description   : Loop through all PotLocater.com state and territory websites to find phone number, business name
##                  address, city, state, zip code, and url of potLocater link
##Python Version: 2.7.11
##Prereqs Knowledge: Python, HTML, CSS, XPath
##Prereqs Hardware: Any computer that has a C++ compiler (libxml2 uses C++)
##Prereqs Software: Python, pip
##Python Libraries: LXML, requests, csv, json, re, os, libxml2, libxslt, datetime
##          Unix install python lib command: "sudo pip install"
##Needed Python file: pyTimer.py
##          pyTimer.py file is found at https://github.com/Test-BMOHB/Media-Monitoring/blob/master/pyTimer.py
##Log file saved at: /var/www/html/Logs/pylog_PotLocator.txt
##CSV file saved at: /var/www/html/mmddyyyy_PotLocator_Scrape.csv
##Run command: sudo python pyScrape_PotLocator.py
##-----------------------------------------------------------------------------
## Version  | mm/dd/yyyy  |  User           |                Changes
##    1       03/01/2016    Justin Suelflow   Initial Draft
##    2       03/07/2016    Justin Suelflow   Datestamp file
##   2.1      03/08/2016    Justin Suelflow   Change datestamp from YYYY-MM-DD to MMDDYYYY
##   2.2      03/30/2016    Justin Suelflow   Updated CSV writer to take out quotes
##   2.3      03/31/2016    Justin Suelflow   Added filename var to send to pyTimer
##   2.4      04/11/2016    Justin Suelflow   Changed log file path
##-----------------------------------------------------------------------------
##*********************END HEADER*********************##

##*********************IMPORT*********************##
##  Import needed python libraries
##  Libraries must be installed using 'pip install'
##  pyTimer is not installed using pip, the standalone file needs to be placed in the same location as this code file
from lxml import html
from lxml.etree import tostring
from datetime import datetime
import requests, csv, re, json, pyTimer, os.path
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
    logFile = open('/var/www/html/Logs/pylog_PotLocator.txt','a')
    logFile.write(text)
##  Close log file
    logFile.close()

##  Function	: createCSV
##  Description	: Writes list to a CSV file
##  Parameters	: liCSV = list type, f1 = file type
##  Returns	:
def createCSV(liCSV):
    writeToLog("Writing to CSV\n")
##  Use the ^ as a delimiter because the data on WeedMaps has lots of other special characters including commas
##  Needed to find a special character that was not used by the data
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

##  Function	: scrapeInfo
##  Description	: Scrapes name, phone number, address, city, state, zip code and url from mainRequest text
##  Parameters	: mainRequest =  = request.post type, loc = string type
##  Returns	: list
def scrapeInfo(requestText, loc):
    li = []
    finList = []
    writeToLog("Scraping " + loc + "\n")
    try:
        requestText = requestText[(requestText.index('Data":') + 6):]
    except:
        writeToLog(requestText)
##  Loop through all characters in the xpath text
##  This loop looks through the text to find the opening and closing brackets to create a proper dictionary
    strDict = ''
    openLi = False
    count = 0
    for t in requestText:
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
            name = ''.join(filter(None, [i["title"]]))
            address = ' '.join(filter(None, [i["address1"],i["address2"]]))
            city = ''.join(filter(None, [i["city"]]))
            state = ''.join(filter(None, [i["state"]]))
            zipcode = ''.join(filter(None, [i["zipcode"]]))
            url = str(i["website"])
            phone = ''.join(filter(None, [i["phone"]]))
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

##*********************MAIN FUNCTION*********************##
##  Function	: main
##  Description	: Opens file and call other functions
##  Parameters	: mainRequest = request.post type, loc = string type, fileName = string type
##  Returns	: 
def main(mainRequest, loc):
    liData = []
##  Add the information that comes from the scrapeInfo function to a list
    requestText = mainRequest.text
    liData.extend(scrapeInfo(requestText, loc))
##  Call function removeDuplicates
    beforeDedup = len(liData)
    liData = removeDuplicates(liData)
    writeToLog(str(len(liData)) + " records of " + str(beforeDedup) + " left after deduplication\n")
##  Call createCSV function to write the list data to the scrapeFile
    createCSV(liData)
##*********************END MAIN FUNCTION********************##

##*********************END FUNCTIONS*********************##

##*********************PROGRAM*********************##
##  If statement makes this program standalone
##  Do not need this if statement if another program will be calling above functions
if __name__ == "__main__":
##  Create start time
    startTime = pyTimer.startTimer()
    writeToLog('***********************************************************************\n')
##  Open a file and overwrite the existing file or create a new file if needed
    currDate = datetime.now()
    fileDate = currDate.strftime('%m%d%Y')
    currDate = currDate.strftime('%Y-%m-%d')
    fileName = '/var/www/html/' + fileDate + '_PotLocator_MMJScrape.csv'
    with open(fileName,'w') as scrapeFile:
        writer = csv.writer(scrapeFile, delimiter='^', quoting=csv.QUOTE_NONE, escapechar=' ')
##  Add a header row to the CSV
        writer.writerow(["Company","PhoneNumber","Address","City","State","ZipCode","Website"])
##  Create list of locations to search
        locations= ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming','Washington DC','Albert','British Columbia','Ontario','Nova Scotia','Quebec','Saskatchewan','Manitoba']
##  Loop through the list of locations to send a http post request to the potlocator api
        for loc in locations:
            mainRequest = requests.post('https://www.potlocator.com/api/searchMarkers', data={'excludeIDs':'','business_type_id':0,'search_key':loc})
            main(mainRequest, loc)
##  Find total time in seconds of program run
    pName = os.path.basename(__file__)
    endTime = pyTimer.endTimer(startTime, pName)
    writeToLog("Program took " + endTime + " to complete.\n")
##*********************END PROGRAM*********************##
