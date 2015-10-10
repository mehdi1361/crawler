__author__ = 'mousavi'
from celery import Celery
import MySQLdb
import datetime

mysql_host = "localhost"
mysql_user = "root"
mysql_pass = "1361522"
mysql_db = "pishnava_crawler"
app = Celery('tasks', broker='amqp://guest@localhost//')
@app.task
def inserttoqueue(page, toneid, tonecode):
    try:
        db = MySQLdb.connect(mysql_host, mysql_user, mysql_pass, mysql_db)
        cursor = db.cursor()
        dateCreated = str(datetime.datetime.now())
        strsql = '''INSERT INTO queues(toneId,toneCode,is_new,page,createdAt,updatedAt) VALUES(%s,%s,%s,%s,'%s','%s');''' % (
            toneid, tonecode, 1, page, dateCreated, dateCreated)
        print strsql
        result = cursor.execute(strsql)
        db.commit()
        db.close()
        # return result
    except Exception:
        print 'duplicate'


def removeduplicate():
    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pass, mysql_db)
    cursor = db.cursor()
    dateCreated = str(datetime.datetime.now())
    strsql = '''delete queues from queues inner join tracks on tracks.toneid=queues.toneid;'''
    result = cursor.execute(strsql)
    db.commit()
    db.close()


def tonesid():
    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pass, mysql_db)
    cursor = db.cursor()
    strsql = '''select toneId,tonecode,page from queues;'''
    cursor.execute(strsql)
    db.commit()
    db.close()
    return cursor.fetchall()


@app.task
def insertotrack(tonecode, tonename, tonesinger, toneprice, tonecredit, tonepublisher, tonegenregroup, tonegenre,
                 toneid, tonepage):
    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pass, mysql_db)
    cursor = db.cursor()
    cursor.execute('set names utf8;')
    strsql = '''select id from tracks where toneId= %s;''' % toneid
    cursor.execute(strsql)
    strsql1 = ''
    if not cursor.rowcount:
        print tonename , toneprice
        strsql1 = '''INSERT INTO tracks(toneId,toneCode,toneName,toneSinger,tonePrice,toneCredit,tonePublisher,toneGenreGroup,toneGenre,tonePage,is_read,is_new,createdAt,updatedAt) VALUES(%s,%s,'%s','%s',%s,%s,'%s','%s','%s',%s,%s,%s, '%s','%s');''' % (toneid, tonecode, tonename.encode('utf8'), tonesinger.encode('utf8'), toneprice.encode('utf8'), tonecredit.encode('utf8'), tonepublisher.encode('utf8'), tonegenregroup.encode('utf8'), tonegenre.encode('utf8'), tonepage, 0, 1, datetime.datetime.now(), datetime.datetime.now())
    else:
        strsql1 = '''update tracks set toneCode=%s ,toneName= %s,toneSinger=%s,tonePrice=%s,toneCredit=%s,tonePublisher=%s,toneGenreGroup=%s ,toneGenre=%s,tonePage=%s,is_read =%s ,is_new = %s where toneId=%s''' % (tonecode, tonename, tonesinger, toneprice, tonecredit, tonepublisher, tonegenregroup, tonegenre, tonepage, 0, 0, toneid)
    print strsql1
    cursor1 = db.cursor()
    cursor1.execute('set names utf8;')
    cursor1.execute(strsql1)
    db.commit()
    db.close()
def truncatequeue():
    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pass, mysql_db)
    cursor = db.cursor()
    cursor.execute('set names utf8;')
    strsql = '''truncate queues;'''
    cursor.execute(strsql)
    db.commit()
    db.close()
    print "truncate queues completed"
