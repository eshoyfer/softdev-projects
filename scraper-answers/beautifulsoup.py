import requests
import re
from bs4 import BeautifulSoup
#pip install beautifulsoup4 and requests on your virtual env
#http://stackoverflow.com/questions/24458353/cleaning-text-string-after-getting-body-text-using-beautifulsoup

#testing beautiful soup on simple request from site
def bsoup():
    r = requests.get("https://answers.yahoo.com/question/index?qid=20080613085817AAqvcNW")
    soup = BeautifulSoup (open(r.content))
    string = soup.findall("div", {"class":"group"})
    print soup.finalall(re.compile("^[A-Z]"))
    print soup.prettify()
    print string


if __name__ == "__main__":
    bsoup()

