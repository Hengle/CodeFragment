#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='graduation',port=3306,charset='utf8')
cur=conn.cursor()
cur2=conn.cursor()

cur.execute('select * from urllist')
item=cur.fetchone()
while item != None:
        team1=item[1]
        team2=item[2]
        infourl=item[4]
        perurl=item[5]
        start=infourl.rfind('/')
        rankurl='http://sports.163.com/special/00051UOC/1soccer163test.html?index_old.php?gid=' + infourl[start + 1:]

        data1=pq(url=infourl)
        #result
        result=data1('#vs').find('span').eq(0).text()	#1-1
        start=result.find('-')
        result = int(result[0:start]) - int(result[start+1:])
	print result

        #vs
	vs=data1('#stat_1').find('td')
	vs_team1win_times = int(vs.eq(1).text())
        vs_team1draw_times = int(vs.eq(2).text())
        vs_team1lose_times = int(vs.eq(3).text())
        vs = vs_team1win_times + vs_team1draw_times + vs_team1lose_times	


cur.close()
cur2.close()
conn.close()

