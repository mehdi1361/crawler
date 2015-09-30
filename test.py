__author__ = 'mousavi'
from FindLastPage import FindPage
from CrawlPage import CrawlPageByPNum
o = FindPage()
s = o.search()
sdat =[]
sdat.append((1, 2))
sdat.append((3, 4))

for i in range(1, int(s) + 1):
    print i
    t = CrawlPageByPNum(i)
    t.find()
print sdat



