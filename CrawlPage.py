# -*- coding: utf-8 -*-
import string
from bs4 import BeautifulSoup
import requests
import re

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))
punctuation_map = lambda A, B: dict((ord(char), B) for char in A)
class Normalizer():
    def __init__(self):
        self.translations = maketrans(
            u'١٢٣٤٥٦٧٨٩٠    ۱۲٣۴۵۶۷۸۹۰٤٥٦₀₁₂₃₄₅₆₇₈₉¹²⁰⁴⁵⁶⁷⁸⁹①②③④⑤⑥⑦⑧⑨⑴⑵⑶⑷⑸⑹⑺⑻⑼⒈⒉⒊⒋⒌⒍⒎⒏⒐٪؛،كيؤئإأآةك',
            u'12345678904560123456789120456789123456789123456789123456789%;,کیویاااهک'
        )
        self.punctuations = punctuation_map(u"ـ\u200E\u200F" + unicode(string.punctuation), u" ")
        IGNORE_CHARS = u'\u0652\u064c\u064d\u064b\u064f\u0650\u064e\u0651\u0653\u0670\u0654\u0621'  # u' ْ ٌ ٍ ً ُ ِ َ ّ ٓ ٰ ٔ ء'
        self.ignore_chars = punctuation_map(IGNORE_CHARS, None)

    def normalize(self, text):
        return text.translate(self.ignore_chars).translate(self.translations).translate(
            self.punctuations).upper().strip()

    def normalize_unique(self, text):
        return self.normalize(text).replace(" ", "").strip()

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

class CrawlPageByPNum(object):
    def __init__(self, PageNumber):
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

        result += self.tonecode.findall(req.text)
        return result

    def find(self):
        result = []
        tests = self.crawl(self._url, self._maxlevel)
        for e in tests:
            # print e
            result.append(e)
        return result


class ToneProcess(object):
    def __init__(self, toneid):
        self._url = 'http://rbt.irancell.ir/user/showDetailPop.do?toneID=%s&fortuneFlag=1&isDownload=0&resServType=1&downdate=undefined&serviceID=undefined&keepThis=true&amp;TB_iframe=true&amp;height=365&amp;width=458/' % toneid
        self._maxlevel = 1
        self.values = re.compile(r'td:last')

    def find(self):
        normal = Normalizer()
        req = requests.get(self._url)
        soup = BeautifulSoup(req.text, 'html.parser')
        rows = soup.findAll('tr')
        for row in rows:
            cells = row.findChildren('td')
            for cell in cells:
                  value = cell.get_text(strip=True).encode('utf8').decode('utf8')
                  # print ord(value[0]), ord(u'٣')
                  print "The value in this cell is %s" % normal.normalize(value)
