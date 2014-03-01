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
                print rankurl
                
                data1=pq(url=infourl)
                #result
                result=data1('#vs').find('span').eq(0).text()	#1-1
                start=result.find('-')
                result = int(result[0:start]) - int(result[start+1:])
                print result

                #rank
                data2 = pq(url=rankurl)
                ranks=data2('#jfpm').find('tr')
                rank1=ranks.eq(1).find('td').eq(1).text()
                rank2=ranks.eq(2).find('td').eq(1).text()
				
                #vs
                vs=data1('#stat_1').find('td')
                vs_team1win_times = int(vs.eq(1).text())
                vs_team1draw_times = int(vs.eq(2).text())
                vs_team1lose_times = int(vs.eq(3).text())
				#对战总数
                vs = vs_team1win_times + vs_team1draw_times + vs_team1lose_times

                #recently
                team1recently = data1('#stat_y2_1').find('td')
                recently_times = team1recently.eq(0).text()
                recently_team1win_times = team1recently.eq(1).text()
                recently_team1draw_times = team1recently.eq(2).text()
                recently_team1lose_times = team1recently.eq(3).text()
                team2recently = data2('#stat_y3_1').find('td')
                recently_team2win_times = team1recently.eq(1).text()
                recently_team2draw_times = team1recently.eq(2).text()
                recently_team2lose_times = team1recently.eq(3).text()

                #next 5 day
                datetime5day = datetime.strptime(date,'%Y-%m-%d') + datetime.timedelta(day = 5)
                trtemp1 = data1('.table_tr1').eq(3).find('tr')
                next5day_team1_match_times = 0
                for m in range(1,len(trtemp1)):
                        trtime = trtemp1.eq(m).find('td').eq(2)
                        start = trtime.find(' ')
                        trtime = trtime[0:start]
                        datetemp = datetime.strptime(date,'%y-%m-%d')
                        if datetemp > datetime5day:
                                break;
                        next5day_team1_match_times = next5day_team1_match_times + 1
					
                trtemp2 = data1('.table_tr2 ').eq(2).find('tr')
                next5day_team2_match_times = 0
                for m in range(2,len(trtemp2)):
                        trtime = trtemp2.eq(m).find('td').eq(2)
                        start = trtime.find(' ')
                        trtime = trtime[0:start]
                        datetemp = datetime.strptime(date,'%y-%m-%d')
                        if datetemp > datetime5day:
                                break;
                        next5day_team2_match_times = next5day_team2_match_times + 1
                        
                #guest
                matchdatas = data2('.f_400')
                #team1
                team1matchdata = matchdatas.eq(0).find('tbody').find('tr')
                team1totalmatchdata = team1matchdata.eq(0).find('td')
                team1_total_wintimes = team1totalmatchdata.eq(1).text()
                team1_total_drawtimes = team1totalmatchdata.eq(3).text()
                team1_total_losetimes = team1totalmatchdata.eq(5).text()
                
                team1mainmatchdata = team1matchdata.eq(1).find('td')
                team1_total_mainwintimes = team1mainmatchdata.eq(1).text()
                team1_total_maindrawtimes = team1mainmatchdata.eq(3).text()
                team1_total_mainlosetimes = team1mainmatchdata.eq(5).text()
                
                team1guestmatchdata = team1matchdata.eq(2).find('td')
                team1_total_guestwintimes = team1guestmatchdata.eq(1).text()
                team1_total_guestdrawtimes = team1guestmatchdata.eq(3).text()
                team1_total_guestlosetimes = team1guestmatchdata.eq(5).text()
                
                #team2
                team2matchdata = matchdatas.eq(1).find('tbody').find('tr')
                team2totalmatchdata = team2matchdata.eq(0).find('td')
                team2_total_wintimes = team2totalmatchdata.eq(1).text()
                team2_total_drawtimes = team2totalmatchdata.eq(3).text()
                team2_total_losetimes = team2totalmatchdata.eq(5).text()
                
                team2mainmatchdata = team2matchdata.eq(1).find('td')
                team2_total_mainwintimes = team2mainmatchdata.eq(1).text()
                team2_total_maindrawtimes = team2mainmatchdata.eq(3).text()
                team2_total_mainlosetimes = team2mainmatchdata.eq(5).text()
                
                team2guestmatchdata = team2matchdata.eq(2).find('td')
                team2_total_guestwintimes = team2guestmatchdata.eq(1).text()
                team2_total_guestdrawtimes = team2guestmatchdata.eq(3).text()
                team2_total_guestlosetimes = team2guestmatchdata.eq(5).text()
                
                
				
        except Exception,ex:
                #cur3.execute('insert into errorlist value(null,%s,%s,%s,%s,%s)',(team1,team2,date,infourl,perurl))
                #conn.commit()
                item=cur.fetchone()
                continue

        
cur.close()
cur2.close()
cur3.close()
conn.close()

