#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq
import urllib2
import gzip
from StringIO import StringIO

from datetime import *
import traceback

curdate = datetime.today().strftime('%Y-%m-%d')

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='graduation',port=3306,charset='utf8')
cur=conn.cursor()
cur2=conn.cursor()
cur3=conn.cursor()

#获得结果
def getResult(data1):
        result=data1('#vs').find('span').eq(0).text()	#1-1
        start=result.find('-')
        print result
        result = int(result[0:start]) - int(result[start+1:])
        return result

#获取排名
def getRank(data2):
        ranks=data2('#jfpm').find('tr')
        rank1=ranks.eq(2).find('td').eq(1).text()
        rank2=ranks.eq(3).find('td').eq(1).text()
        return (int(rank1), int(rank2))

#获取最近比赛，data，标签
def getRecently(data1,label,index1):
        teamrecently = data1(label).eq(index1).find('tr')
        recently_times = len(teamrecently) - 1
        recently_teamwin_times = 0
        recently_teamdraw_times = 0
        recently_teamlose_times = 0

        for i in range(1,len(teamrecently)):
                tdtmp=teamrecently.find('td').eq(7).text()
                print tdtmp
                if(cmp(tdtmp,'胜') == 0):
                        recently_teamwin_times = recently_teamwin_times + 1
                elif(cmp(tdtmp,'平') == 0):
                        recently_teamdraw_times = recently_teamdraw_times + 1
                else:
                        recently_teamlose_times = recently_teamlose_times + 1
        print "getRecently" + str(recently_teamwin_times) + ',' + str(recently_teamdraw_times) + ',' + str(recently_teamlose_times)
        return (recently_times,recently_teamwin_times,recently_teamdraw_times,recently_teamlose_times)

#获取未来五天，data，标签   data1,date,'.table_tr1',3   data1,date,'.table_tr2',2
def getNextFiveDays(data1,date,label,index1):
	datetime5day = datetime.strptime(date,'%Y-%m-%d') + datetime.timedelta(day = 5)
	trtemp = data1(label).eq(index1).find('tr')
	next5day_team_match_times = 0
	for m in range(1,len(trtemp)):
		trtime = trtemp.eq(m).find('td').eq(2)
		start = trtime.find(' ')
		trtime = trtime[0:start]
		datetemp = datetime.strptime(date,'%y-%m-%d')
		if datetemp > datetime5day:
			break;
		next5day_team_match_times = next5day_team_match_times + 1
	print "getNextFiveDays"
	return next5day_team_match_times

#获取比赛数据
def getMatchData(data2, index1):
	teamtotalmatchdata = data2.eq(index1).find('td')
	team_total_wintimes = teamtotalmatchdata.eq(1).text()
	team_total_drawtimes = teamtotalmatchdata.eq(3).text()
	team_total_losetimes = teamtotalmatchdata.eq(5).text()
	print "matchdata:" + team_total_wintimes + ',' + team_total_drawtimes + ',' + team_total_drawtimes 
	return (int(team_total_wintimes),int(team_total_drawtimes),int(team_total_losetimes))

#获取赔率
def getPercent(data3):
        alllist=data3('.table_normal').find('td')
        winper = alllist.eq(5).text()
        drawper = alllist.eq(6).text()
        loseper = alllist.eq(7).text()
        print "Percent:" + winper + ',' + drawper + ',' + loseper 
        return (int(winper), int(drawper), int(loseper))

def getData(url):
        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept-Encoding':'gzip'  }
        req = urllib2.Request(url,headers=req_header)
        html = urllib2.urlopen(req).read()
        bi = StringIO(html)
        gf = gzip.GzipFile(fileobj=bi)
        return gf.read().decode('utf-8')

cur.execute('select * from urllist')
item=cur.fetchone()
while item != None:
        try:
                team1=item[2]
                team2=item[3]
                date=item[4]
                infourl=item[5]
                perurl=item[6]
                print team1 + ',' + team2 + ',' + date + ',' + infourl + ',' + perurl
                if date >= curdate:
                        print 'date is not history.'
                        item = cur.fetchone()
                        continue
                
                start=infourl.rfind('/')
                rankurl='http://163.1soccer.com/index_old.php?gid=' + infourl[start + 1:]
                
                value = []

                tmpdata=getData(infourl)		
                data1 = pq(tmpdata)
                
                #result
                result = getResult(data1)
                print 'result:' + str(result)
		
                
		
                #vs
                vs=data1('#stat_1').find('td')
                vs_team1win_times = int(vs.eq(1).text())
                vs_team1draw_times = int(vs.eq(2).text())
                vs_team1lose_times = int(vs.eq(3).text())
		#对战总数
                vs = vs_team1win_times + vs_team1draw_times + vs_team1lose_times
                print 'vs:' + str(vs) +',' + str(vs_team1win_times) + ',' + str(vs_team1draw_times) + ',' + str(vs_team1lose_times)
                
                #recently
                recently_times,recently_team1win_times,recently_team1draw_times,recently_team1lose_times = getRecently(data1,'.table_tr1',2)
                
                recently_times,recently_team2win_times,recently_team2draw_times,recently_team2lose_times = getRecently(data1,'.table_tr2',1)

                #next 5 day
                next5day_team1_match_times = getNextFiveDays(data1,date,'.table_tr1',3)
                
                next5day_team2_match_times = getNextFiveDays(data1,date,'.table_tr2',2)

                
                data2 = pq(url=rankurl)
                
                #rank
                rank1,rank2 = getRank(data2)
                print 'team1 rank:' + str(rank1) + ', team2 rank:' + str(rank2)
                
                #guest
                matchdatas = data2('.f_400')
                #team1
                team1matchdata = matchdatas.eq(0).find('tbody').find('tr')
                team1_total_wintimes,team1_total_drawtimes,team1_total_losetimes = getMatchData(team1matchdata, 0)
                team1_total_mainwintimes,team1_total_maindrawtimes,team1_total_mainlosetimes = getMatchData(team1matchdata, 1)
                team1_total_guestwintimes,team1_total_guestdrawtimes,team1_total_guestlosetimes = getMatchData(team1matchdata, 2)

                #team2
                team2matchdata = matchdatas.eq(1).find('tbody').find('tr')
                team2_total_wintimes,team2_total_drawtimes,team2_total_losetimes = getMatchData(team2matchdata, 0)
                team2_total_mainwintimes,team2_total_maindrawtimes,team2_total_mainlosetimes = getMatchData(team2matchdata, 1)
                team2_total_guestwintimes,team2_total_guestdrawtimes,team2_total_guestlosetimes = getMatchData(team2matchdata, 2)
        	
                data3 = pq(url=perurl)
                #percent
                team1_win_percent,team1_draw_percent,team1_lose_percent = getPercent(data3)
        except Exception,ex:
                # cur3.execute('insert into errorlist value(null,%s,%s,%s,%s,%s)',(team1,team2,date,infourl,perurl))
                # conn.commit()
                print Exception,":",ex
                print ''
                item=cur.fetchone()
                continue
        item = cur.fetchone()
cur.close()
cur2.close()
cur3.close()
conn.close()

