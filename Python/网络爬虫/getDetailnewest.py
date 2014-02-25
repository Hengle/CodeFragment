#encoding=utf-8
import MySQLdb
from pyquery import PyQuery as pq
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
    result = int(result[0:start]) - int(result[start+1:])
    print result
	return result
end
#获取排名
def getRank(data2):
    ranks=data2('#jfpm').find('tr')
	rank1=ranks.eq(1).find('td').eq(1).text()
	rank2=ranks.eq(2).find('td').eq(1).text()
	return (int(rank1), int(rank2))
end
#获取最近比赛，data，标签
def getRecently(data1,label):
	teamrecently = data1(label).find('td')
	recently_times = teamrecently.eq(0).text()
	recently_teamwin_times = teamrecently.eq(1).text()
	recently_teamdraw_times = teamrecently.eq(2).text()
	recently_teamlose_times = teamrecently.eq(3).text()
	return (int(recently_times),int(recently_teamwin_times),int(recently_teamdraw_times),int(recently_teamlose_times))
end
#获取未来五天，data，标签
def getRecently(data1,date,label,index1):
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
	return next5day_team_match_times
end
def getMatchData(data2, index1)
	teamtotalmatchdata = data2.eq(index1).find('td')
	team_total_wintimes = teamtotalmatchdata.eq(1).text()
	team_total_drawtimes = teamtotalmatchdata.eq(3).text()
	team_total_losetimes = teamtotalmatchdata.eq(5).text()
	return (int(team_total_wintimes),int(team_total_drawtimes),int(team_total_losetimes))
end
cur.execute('select * from urllist')
item=cur.fetchone()
while item != None:
        try:
                team1=item[2]
                team2=item[3]
                date=item[4]
                infourl=item[5]
                perurl=item[6]
                if date > curdate:
                        item = cur.fetchone()
                        continue
                
                start=infourl.rfind('/')
                rankurl='http://163.1soccer.com/index_old.php?gid=' + infourl[start + 1:]
                
				value = []
				
                data1=pq(url=infourl)
                data2 = pq(url=rankurl)
				
                #result
				result = getResult(data1)
				
                #rank
				rank1,rank2 = getRank(data2)
			
                #vs
                vs=data1('#stat_1').find('td')
                vs_team1win_times = int(vs.eq(1).text())
                vs_team1draw_times = int(vs.eq(2).text())
                vs_team1lose_times = int(vs.eq(3).text())
				#对战总数
                vs = vs_team1win_times + vs_team1draw_times + vs_team1lose_times

				#recently
				recently_times,recently_team1win_times,recently_team1draw_times,recently_team1lose_times = getRecently(data1,'#stat_y2_1')
				
				recently_times,recently_team2win_times,recently_team2draw_times,recently_team2lose_times = getRecently(data1,'#stat_y3_1')

				#next 5 day
				next5day_team1_match_times = getRecently(data1,date,'.table_tr1',3)
				
				next5day_team2_match_times = getRecently(data1,date,'.table_tr2',2)
					
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

        except Exception,ex:
                cur3.execute('insert into errorlist value(null,%s,%s,%s,%s,%s)',(team1,team2,date,infourl,perurl))
                conn.commit()
                item=cur.fetchone()
                continue

        
cur.close()
cur2.close()
cur3.close()
conn.close()

