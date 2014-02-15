#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='graduation',port=3306,charset='utf8')
cur=conn.cursor()
content=pq(url='http://163.1soccer.com/lottery_list.php')
data1=content('.his_links')

errorissue=7050
flag=True

for i in range(0,len(data1)):
    data2=data1.eq(i).children()
    for j in range(0,len(data2)):
        issue=data2.eq(j).text()
        print issue
        
        if int(issue) == errorissue:
            flag=False
        if flag:
            continue
        
        url1=data2.eq(j).attr('href')
        start=url1.find('isu=') + 4
        end=url1.rfind('&')
        temp=url1[start:end]
        url2='http://163.1soccer.com/lottery.php?isu=' + temp
        print 'issue:' + temp
        content2=pq(url=url2)
        header=content2('.table_header')
        info=content2('.table_info')
        for k in range(0,len(header)):
            finalurl=header.eq(k).find('a').eq(2).attr('href')
            index=finalurl.rfind('=')
            gid=finalurl[index + 1:]
            infourl='http://www.1soccer.com/index.php/info/index/id/' + gid
            perurl='http://www.1soccer.com/odds/detail/id/' + gid
            team=header.eq(k).find('a').eq(1).text()
            mid=team.find('vs')
            team1=team[0:mid-1]
            team2=team[mid+3:]
            timetemp=info.eq(k).text()
            time=timetemp[5:]
            print team1 + ',' + team2 + ',' + time + ',' + gid
            cur.execute('insert into urllist values(null,%s,%s,%s,%s,%s,%s)',(issue,team1,team2,time,infourl,perurl))
            conn.commit()
cur.close()
conn.close()

