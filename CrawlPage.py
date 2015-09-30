import requests
import re

class CrawlPageByPNum(object):
    def __init__(self,PageNumber):
        self._url = 'http://rbt.irancell.ir/user/browseordinarybyname.do?orderBy=2&urlFlag=101&uploadType=&resourceServiceType=1&toneNameLetter=&page=%s' % PageNumber
        self._maxlevel = 1
        self.toneid = re.compile(r'value="(.*)"  class="icon_play"')
        self.tonecode = re.compile(r'<a href="###" onclick="showToneDetails\(this,(.*),')

    def crawl(self, url, maxlevel):
        if maxlevel == 0:
            return
        req = requests.get(url)
        result = []
        # Check if successful
        if req.status_code != 200:
            return []

        # result += self.toneid.findall(req.text)
        result += self.tonecode.findall(req.text)
        return result

    def find(self):
        tests = self.crawl(self._url, self._maxlevel)
        for e in tests:
            print e
            stringcount = e
        # return stringcount
