from flask import Flask, render_template, request, url_for
import google
import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
import filterNames
from collections import Counter
from socket import timeout
from ssl import SSLError
import getDate

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/answer", methods=["GET"])
def answer():
    query = request.args.get('q')
    query_upper = query.upper()
    if query_upper.find("WHO") > -1:
        try:
            urls = [x for x in google.search(query, lang='en', num=10, start=0, stop=9, pause=1.0)]
        except urllib2.URLError:
            pass
        print "Got urls :)"
        pages = []
        retStr = "<body bgcolor='C0C0C0'>"
        topNames = Counter() 
        for url in urls[:10]:
            try:
                soup = BeautifulSoup(urlopen(url, timeout=1).read())
            except urllib2.URLError:
                continue
            except timeout:
                continue
            except SSLError:
                continue
            print "Got soup :)"
            pages.append(soup.get_text())
        len_pages = len(pages)
        for pageIndex in range(len_pages):
            NUM_RESULTS = 5
            names = filterNames.getFilteredInputList(pages[pageIndex]).most_common(NUM_RESULTS)
            retStr += "<table border='1'><tr><td>Name</td><td>Frequency</td></tr>"
            for index in range(len(names)):
                name = names[index][0]
                if not(name.upper() in query_upper):
                    if not(' ' in name):
                        for item in topNames:
                            parts = item.split(" ")
                            if len(parts) > 1:
                                if name in parts:
                                    topNames[item] += 1
                                    print "Increasing confidence of " + item + " with " + name
                    topNames[name] += len_pages - pageIndex + NUM_RESULTS - index 
                    retStr += "<tr><td>" + name + "</td><td>" + str(names[index][1]) + "</td></tr>"
            retStr += "</table>"
        retStr = "<h1 style='color:blue'>The most common name was " + topNames.most_common(1)[0][0] + "</h1>" + retStr + "</body>"

        return retStr

    elif query.upper().find("WHEN") > -1:
        try:
            urls = [x for x in google.search(query, lang='en', num=10, start=0, stop=9, pause=1.0)]
        except urllib2.URLError:
            pass
        print "Got urls :)"
        pages = []
        retStr = "<body bgcolor='C0C0C0'>"
        topdt = Counter()
        for url in urls:
            try:
                soup = BeautifulSoup(urlopen(url, timeout=1).read())
            except urllib2.URLError:
                continue
            except timeout:
                continue
            except SSLError:
                continue
            print "Got soup :)"
            pages.append(soup.get_text())
            for page in pages:
                dts = getDate.filterDateandTime(page).most_common(10)
                if len(dts) > 0:
                    dt = dts[0][0]
                    if not(' ' in dt):
                        for item in topdt:
                            parts = item.split(" ")
                            if len(parts) > 1:
                                if dt in parts:
                                    topdt[item] += 1
                                    print "Increasing confidence of " + item + " with " + dt
                    topdt[dt] += 1
            retStr += "<table border='1'><tr><td>Date/Time</td><td>Frequency</td></tr>"
            for _tuple in dts:
                retStr += "<tr><td>" + _tuple[0] + "</td><td>" + str(_tuple[1]) + "</td></tr>"
            retStr += "</table>"
        retStr = "<h1 style='color:blue'>The most common date or time  was " + topdt.most_common(1)[0][0] + "</h1>" + retStr + "</body>"
        return retStr

    elif query_upper.find("WHERE") > -1:
        if "AM" in query_upper or "am" in query_upper:
        # Self referential case
            JSurl = url_for('static', filename='mylocation.js')
            retStr = '<script src="' + JSurl + '"></script>'
            return retStr
        else:
            try:
                urls = [x for x in google.search(query, lang='en', num=10, start=0, stop=9, pause=1.0)]
            except urllib2.URLError:
                pass
            print "Viable URLs found"
            retStr = ""
            pages = []
            stored = []
            try:
                true_query = query_upper.split(' ')[2:]
            except:
                true_query = query_upper.split(' ')[-2:]
            for url in urls[:10]:
                try:
                    soup = BeautifulSoup(urlopen(url, timeout=1).read())
                except urllib2.URLError:
                    continue
                except timeout:
                    continue
                except SSLError:
                    continue
                print "Soup's up"
            try:
                pages.append(soup.get_text())
            except:
                return "Nothing found :("
            for page in pages:
                sentences = page.split('.')
                potential_keywords = ['location', 'position', 'find', 'address', 'residence', 'coordinates', 'coordinate', 'neighborhood']
                for sentence in sentences:
                    for keyword in potential_keywords:
                        if keyword in sentence or keyword.title() in sentence:
                            # Since it was sorted by prioritized pages,
                            # We'll use that as the rank (first found = better)
                            try:
                                print sentence, keyword, "SUCCESS"
                            except:
                                print "encoding error in printing to console"
                            stored += [sentence]
            try: 
                retStr = "The most likely answer is: " + stored[0]
            except:
                retStr = "Nothing found :("
            return retStr


#    elif query_upper.find("WHEN") > -1:
#        try:
#            urls = [x for x in google.search(query, lang='en', num=10, start=0, stop=9, pause=1.0)]
#        except urllib2.URLError:
#            pass
#        print "Viable URLs found"
#        retStr = ""
#        pages = []
#        stored = []
#        try:
#            true_query = query_upper.split(' ')[2:]
#        except:
#            true_query = query_upper.split(' ')[-2:]
#        for url in urls[:10]:
#            try:
#                soup = BeautifulSoup(urlopen(url, timeout=1).read())
#            except urllib2.URLError:
#                continue
#            except timeout:
#                continue
#            except SSLError:
#                continue
#            print "Soup's up"
#        try:
#            pages.append(soup.get_text())
#        except:
#            return "Nothing found :("
#        for page in pages:
#            sentences = page.split('.')
#            potential_keywords = ['time', 'date', 'schedule', 'when', 'year', 'month', 'day', 'year']
#            for sentence in sentences:
#                for keyword in potential_keywords:
#                    if keyword in sentence or keyword.title() in sentence:
                        # Since it was sorted by prioritized pages and keywords,
                        # We'll use that as the rank (first found = naturally better)
#                        stored += [sentence]
#        try:
#            retStr = "The most likely answer is: " +stored[0]
#        except:
#            retStr = "Nothing found :("
#        return retStr
    else:
        return "Query not supported"
    #return render_template("answer.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
