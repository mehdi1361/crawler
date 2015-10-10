
from CrawlPage import *
import memcache
from DbOp import *
import subprocess

class Caching(object):
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server = memcache.Client([self.hostname])

    def set(self, key, value, expiry=900):
        self.server.set(key, value, expiry)

    def get(self, key):
        return self.server.get(key)

    def delete(self, key):
        self.server.delete(key)

o = FindPage()
AllPageNumber = o.search()
# AllPageNumber = 6

r = []
checkcache = Caching()
# checkcache.server.flush_all()
for i in range(1, int(AllPageNumber) + 1):
    try:
        t = CrawlPageByPNum(i)
        r = t.find()
        print 'page number:%s' % i
        for j in r:
            j = j.split(',')
            toneid = int(j[0].replace("'", ""))
            strtonecode = str(int(j[1].replace("'", "")))
            toncode = '%s%s' % (strtonecode[3:6], int(strtonecode[-8:]))
            s = checkcache.get(str(toneid))
            if s is None:
                print 'in if statement'
                checkcache.set(str(toneid), toncode)
                inserttoqueue(int(i), int(toneid), int(toncode))
            print toneid, toncode

    except Exception:
        print 'error'
removeduplicate()
listd = tonesid()
c = 0
for i in listd:
        print 'toneid:%s and toncode: %s' % (i[0], i[1])
        proc = ToneProcess(i[0])
        lstp = proc.find()
        insertotrack(i[1], lstp[1], lstp[2], lstp[3], lstp[4], lstp[5], lstp[6], lstp[7], i[0], i[2])

# subprocess.call("php artsian sync:crawled && artsian sync:file")
