#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='graduation',port=3306,charset='utf8')
cur=conn.cursor()
cur2=conn.cursor()

cur.execute("select * from url_list")
item=cur.fetchone()
while item != None:
    oldurl=item[5]
    index=oldurl.rfind('=')
    gid=oldurl[index + 1:]
    infourl='http://www.1soccer.com/index.php/info/index/id/' + gid
    perurl='http://www.1soccer.com/odds/detail/id/392223' + gid
    cur2.execute('insert into urllist values(null,%s,%s,%s,%s,%s,%s)',(item[1],item[2],item[3],item[4],infourl,perurl))
    item=cur.fetchone()
conn.commit()
cur.close()
conn.close()

