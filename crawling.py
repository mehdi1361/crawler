import requests
import re
from bs4 import BeautifulSoup
pageumber = re.compile(r'gotoPage\(1,0,(.*)\);')
link_re = re.compile(r'href="(.*?)"')

def crawl(url, maxlevel):
    # Limit the recursion, we're not downloading the whole Internet
    if(maxlevel == 0):
        return

    # Get the webpage
    req = requests.get(url)
    result = []

    # Check if successful
    if(req.status_code != 200):
        return []

    result += pageumber.findall(req.text)
    return result

tests = crawl('http://rbt.irancell.ir/user/browseordinarybyname.do?resourceServiceType=1&urlFlag=101&orderBy=',1)
print "Scrapped pagecount addresses:"
for e in tests:
    stringcount = e
print stringcount

