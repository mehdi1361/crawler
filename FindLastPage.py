import requests
import re

class FindPage(object):
    def __init__(self):
        self._url = 'http://rbt.irancell.ir/user/browseordinarybyname.do?resourceServiceType=1&urlFlag=101&orderBy='
        self._maxlevel = 1
        self.pageumber = re.compile(r'gotoPage\(1,0,(.*)\);')

    def crawl(self, url, maxlevel):
        if maxlevel == 0:
            return
        req = requests.get(url)
        result = []
        # Check if successful
        if req.status_code != 200:
            return []

        result += self.pageumber.findall(req.text)
        return result

    def search(self):

        tests = self.crawl(self._url, self._maxlevel)
        for e in tests:
            stringcount = e
        return stringcount
