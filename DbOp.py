__author__ = 'mousavi'
from celery import Celery
import MySQLdb
import datetime
import memcache
app = Celery('tasks', broker='amqp://guest@localhost//')
@app.task
def inserttoqueue(page, toneid, tonecode):
    db = MySQLdb.connect("localhost", "root", "1361522", "pishnav_crawler")
    cursor = db.cursor()
    dateCreated = str(datetime.datetime.now())
    strsql = '''INSERT INTO queues(toneId,toneCode,is_new,page,createdAt,updatedAt) VALUES(%s,%s,%s,%s,'%s','%s');''' % (toneid, tonecode, 1, page, dateCreated, dateCreated)
    print strsql
    result = cursor.execute(strsql)
    db.commit()
    db.close()
    # return result

def removeduplicate():
    # ;
    db = MySQLdb.connect("localhost", "root", "1361522", "pishnav_crawler")
    cursor = db.cursor()
    dateCreated = str(datetime.datetime.now())
    strsql = '''delete queues from queues inner join tracks on tracks.toneid=queues.toneid;'''
    result = cursor.execute(strsql)
    db.commit()
    db.close()

def tonesid():
    db = MySQLdb.connect("localhost", "root", "1361522", "pishnav_crawler")
    cursor = db.cursor()
    strsql = '''select toneId,tonecode from queues;'''
    cursor.execute(strsql)
    db.commit()
    db.close()
    return cursor.fetchall()

@app.task
def insertotrack(toneid):
    db = MySQLdb.connect("localhost", "root", "1361522", "pishnav_crawler")
    cursor = db.cursor()
    dateCreated = str(datetime.datetime.now())
    strsql = '''select * from tracks where toneId= %s;''' % toneid
    cursor.execute(strsql)

    strsql1=''
    dateproceed = str(datetime.datetime.now())
    if not cursor.rowcount:
        print 'no row'
        # strsql1 = '''INSERT INTO queues(toneId,toneCode,is_new,page,createdAt,updatedAt) VALUES(%s,%s,%s,%s,'%s','%s');''' % (toneid, tonecode, 1, page, dateCreated, dateCreated)
    else:
        print 'found'
        # strsql1 = '''INSERT INTO queues(toneId,toneCode,is_new,page,createdAt,updatedAt) VALUES(%s,%s,%s,%s,'%s','%s');''' % (toneid, tonecode, 1, page, dateCreated, dateCreated)
    # cursor1 = db.cursor()
    #
    # cursor1.execute(strsql1)
    db.commit()
    db.close()