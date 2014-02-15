#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='music',port=3306,charset='utf8')
cur=conn.cursor()
cur2=conn.cursor()
cur3=conn.cursor()

#cur.execute('insert into videoList values(null,%s)',('http://tv.cntv.cn/video/C33763/2771152813b04588a27b00dfb809cc8f'))
#conn.commit()
cur.execute('select * from videoList')
videourl=cur.fetchone()
while videourl != None:
    print 'video url:' + str(videourl[0])
    videourl=videourl[1]
    content=pq(url=videourl)
    data=content('.shouhang')
    conststr2='《'
    conststr3='》'
    if len(data) > 0:
        data2 = data.eq(0).text()
        items=data2.split(conststr2.decode('utf8'))
        for j in range(1,len(items)):
            item=items[j]
            end1=item.find(conststr3.decode('utf8'))
            name=item[0:end1]
            end2=item.find('\n')
            if end2 != -1:
                player=item[end1+5:end2]
            else:             
                player=''
            print name + ',' + player
            cur2.execute('select * from music_list where musicName=%s',(name))
            num = len(cur2.fetchall())
            print num
            if num == 0:
                cur3.execute('insert into music_list values(null,%s,%s)',(name,player))
                conn.commit()
    videourl=cur.fetchone()
conn.commit()
cur.close()
cur2.close()
cur3.close()
conn.close()

