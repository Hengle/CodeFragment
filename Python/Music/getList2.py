#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='music',port=3306,charset='utf8')
cur=conn.cursor()

temp='http://tv.cntv.cn/videoset/C33763/page/'

for i in range(1,20):
    videourl=temp + str(i)
    content=pq(url=videourl)
    data=content('.image_list').find('li')
    for j in range(0,len(data)):
        url='http://tv.cntv.cn' + data.eq(j).find('a').eq(0).attr('href')
        print url
        cur.execute('insert into videoList values(null,%s)',(url))
            
conn.commit()
cur.close()
conn.close()

