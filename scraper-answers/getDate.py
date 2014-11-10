import re
from collections import Counter
import time

def filterDateandTime (r):
    #creates a counter that will be used to find the frequency of the results
    results = Counter()
#source http://stackoverflow.com/questions/10086980/date-matching-using-python-regex
    regex_dates = "\d{1,2}[-/:]\d{1,2}[-/:]\d{2,4}"
    regex = re.compile(regex_dates)
    datestimes = regex.findall (r)
    for a in findDate(r):
        datestimes.append(a)
    #print datestimes
    for b in findTime(r):
        datestimes.append(b)
    for c in datestimes:
        results [c] += 1
    return results
    

def findDate(r):
    #only finds phrases like January 24, 1900
    listOfDates = re.findall("(?:(January|February|March|April|May|June|July|August|September|October|November|December) +(0?[1-9]|[12]\d|3[01])?, *([0-9]*)?)", r)
    listdates =[] 

    for l in listOfDates:
        listdates.append( l [0] + " " + l[1] + ", " + l[2])
        
    return listdates

def findTime(r):
    #finds phrases with 1 or 2 digits, then a : then 1 or 2 more digits
    listOfTimes = re.findall("\d{1,2}[:]\d{1,2}", r)
    return listOfTimes


if __name__ == "__main__":
    r = findDate("January 29, 2014, January 15, 2013")
    print (r)
    r = findTime("9:30")
    print (r)
    r = filterDateandTime("10:30 11-11-2012 11/12/2014 January 29, 2014, January 15, 2013")
    print(r)
