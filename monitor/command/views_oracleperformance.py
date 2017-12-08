#! /usr/bin/python
import redis
import time
import MySQLdb
import datetime
import pandas as pd
def oracle_performance_week(performance_type,ipaddress_tnsname_list,starttime,endtime,interval):
    final_series=[]
    format = '%Y-%m-%d %H:%M:%S'
    x=[]
    for starttime1 in range(starttime,endtime+1,604800):
        timearray=time.localtime(starttime1)
        dt = time.strftime(format, timearray).split()
        dt_week=dt[0].split('-')
        week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1]
        x.append(week)

    for ipaddress_tnsname in ipaddress_tnsname_list:
        key=performance_type+'='+ipaddress_tnsname.split(':')[0]+'='+ipaddress_tnsname.split(':')[1]
        if performance_type in ['LogicalReads','PhysicalReads']:
            unit=3600*24
        elif performance_type=='DBTime':
            unit=60000000
        elif performance_type in ['SortsDisk','FetchContinuedRow','FetchByRowid']:
            unit=1
        elif performance_type =='CPUTime':
            unit=60000
        else:
            unit=3600*24
        redisConn=redis.StrictRedis()
        format = '%Y-%m-%d %H:%M:%S'
        ddate=[]
        dtime=[]
        dvalue=[]
        dweek=[]
        series_singal={}
        result=redisConn.lrange(key,0,-1)
        for i in result:
            j=i.decode().split(':')
            if int(j[0]) >=int(starttime) and int(j[0])<=int(endtime):
                value= time.localtime(int(j[0]))
                dt = time.strftime(format, value).split()
                dt_week=dt[0].split('-')
                week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1] #caculate date's week 
                dweek.append(week)
                ddate.append(dt[0])
                dtime.append(dt[1])
                dvalue.append(int(j[1])/unit/7)
        result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'value':dvalue})
        week_df=result['value'].groupby(result['week'])
        week_result=(week_df.first() - week_df.last())/unit
        series_reindex=pd.DataFrame({'week':week_result.index.values.tolist(),'value':week_result.values.tolist()})
        series_reindex.set_index('week',inplace=True)
        s=series_reindex.reindex(x,fill_value=0)
        series_singal['name']=ipaddress_tnsname
        series_singal['data']= s['value'].values.tolist()
        series_singal['x']=s.index.values.tolist()
        final_series.append(series_singal)
    return final_series
def oracle_performance_day(performance_type,ipaddress_tnsname_list,starttime,endtime,interval):
    final_series=[]
    x=[]
    #series_singal={}
    for starttime1 in range(starttime,endtime+1,86400):
        timearray=time.localtime(starttime1)
        x.append(time.strftime("%Y-%m-%d",timearray))

    for ipaddress_tnsname in ipaddress_tnsname_list:
        key=performance_type+'='+ipaddress_tnsname.split(':')[0]+'='+ipaddress_tnsname.split(':')[1]
        if performance_type in ['LogicalReads','PhysicalReads']:
            unit=3600*24
        elif performance_type=='DBTime':
            unit=60000000
        elif performance_type in ['SortsDisk','FetchContinuedRow','FetchByRowid']:
            unit=24
        elif performance_type =='CPUTime':
            unit=6000
        else:
            unit=3600*24
        redisConn=redis.StrictRedis()
        format = '%Y-%m-%d %H:%M:%S'
        ddate=[]
        dtime=[]
        dvalue=[]
        dweek=[]
        series_singal={}
        result=redisConn.lrange(key,0,3600)
        for i in result:
            j=i.decode().split(':') #b'1511157600:175548353'
            #return j[1]
            if int(j[0]) >=starttime and int(j[0])<endtime+86400:
                value= time.localtime(int(j[0])) #time.struct_time(tm_year=2017, tm_mon=11, tm_mday=19, tm_hour=14
                dt = time.strftime(format, value).split() # before split format 2017-11-19 14:21:03
                dt_week=dt[0].split('-')
                week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1]  #caculate datte's week
                dweek.append(week)
                ddate.append(dt[0])
                dtime.append(dt[1])
                dvalue.append(int(j[1]))
        #return dvalue
        result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'value':dvalue})
        day_df=result['value'].groupby(result['date'])
        day_result=(day_df.max() - day_df.min())/unit
        series_reindex=pd.DataFrame({'date':day_result.index.values.tolist(),'value':day_result.values.tolist()})
        series_reindex.set_index('date',inplace=True)
        s=series_reindex.reindex(x,fill_value=series_reindex['value'].mean())
        series_singal['name']=ipaddress_tnsname
        series_singal['data']= s['value'].values.tolist()
        series_singal['x']=s.index.values.tolist()
        final_series.append(series_singal)
    return final_series


def oracle_topevent_day_avg_wait(performance_type,ipaddress_tnsname_list,starttime,endtime):
    final_series=[]
    for ipaddress_tnsname in ipaddress_tnsname_list:
        ipaddress=ipaddress_tnsname.split(':')[0]
        tnsname=ipaddress_tnsname.split(':')[1]
        unit=100
        sql='SELECT sql_time,wait_time,total_timeouts,total_waits FROM oracle.oracle_oracle_topevent where ipaddress=\''+ipaddress+'\'  and tnsname=\''+tnsname+'\'  AND EVENT_NAME=\''+performance_type+'\'  order by sql_time desc'
        db = MySQLdb.connect("localhost","root","123456","oracle")
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        ddate=[]
        dtime=[]
        dweek=[]
        wait_time=[]
        total_timeouts=[]
        total_waits=[]
        format = '%Y-%m-%d %H:%M:%S'
        series_singal={}
        for j in result:
            if int(j[0]) >=int(starttime) and int(j[0])<=int(endtime):
                value= time.localtime(int(j[0]))
                dt = time.strftime(format, value).split()
                dt_week=dt[0].split('-')
                week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1]
                dweek.append(week)
                ddate.append(dt[0])
                dtime.append(dt[1])
                wait_time.append(int(j[1])/unit)
                total_timeouts.append(int(j[2]))
                total_waits.append(int(j[3]))
        result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'wait_time':wait_time,'total_timeouts':total_timeouts,'total_waits':total_waits})
        day_df=result.groupby('date')['total_timeouts','total_waits','wait_time'].first()-result.groupby('date')['total_timeouts','total_waits','wait_time'].last()
        day_df['avg_wait']=(day_df['wait_time']/day_df['total_waits'])*1000
        day_df=day_df.fillna(0)
        series_singal['name']=ipaddress_tnsname
        series_singal['data']= day_df.avg_wait.tolist()
        series_singal['x']=day_df.index.values.tolist()
        final_series.append(series_singal)
    return final_series


def oracle_topevent_hour_total_waits(performance_type,ipaddress_tnsname_list,starttime,endtime):
    final_series=[]
    for ipaddress_tnsname in ipaddress_tnsname_list:
        ipaddress=ipaddress_tnsname.split(':')[0]
        tnsname=ipaddress_tnsname.split(':')[1]
        unit=100
        sql='SELECT sql_time,wait_time,total_timeouts,total_waits FROM oracle.oracle_oracle_topevent where ipaddress=\''+ipaddress+'\'  and tnsname=\''+tnsname+'\'  AND EVENT_NAME=\''+performance_type+'\'  order by sql_time desc'
        db = MySQLdb.connect("localhost","root","123456","oracle")
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        ddate=[]
        dtime=[]
        dweek=[]
        wait_time=[]
        total_timeouts=[]
        total_waits=[]
        format = '%Y-%m-%d %H:%M:%S'
        series_singal={}
        for j in result:
            if int(j[0]) >=int(starttime) and int(j[0])<=int(endtime)+10:
                value= time.localtime(int(j[0]))
                dt = time.strftime(format, value).split()
                dt_week=dt[0].split('-')
                week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1]
                dweek.append(week)
                ddate.append(dt[0])
                dtime.append(dt[1])
                wait_time.append(int(j[1])/unit)
                total_timeouts.append(int(j[2]))
                total_waits.append(int(j[3]))
        result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'wait_time':wait_time,'total_timeouts':total_timeouts,'total_waits':total_waits})
        length=result['date'].count()
        data=[]
        for i in range(0,length-1):
            j= result.loc[i]['total_waits']-result.loc[i+1]['total_waits']
            data.append(j)
        data.reverse()
        #day_df['avg_wait']=(day_df['wait_time']/day_df['total_waits'])*1000
        series_singal['name']=ipaddress_tnsname
        series_singal['data']= data
        final_series.append(series_singal)
    return final_series
def oracle_topevent_day_total_waits(performance_type,ipaddress_tnsname_list,starttime,endtime):
    final_series=[]
    for ipaddress_tnsname in ipaddress_tnsname_list:
        ipaddress=ipaddress_tnsname.split(':')[0]
        tnsname=ipaddress_tnsname.split(':')[1]
        unit=100
        sql='SELECT sql_time,wait_time,total_timeouts,total_waits FROM oracle.oracle_oracle_topevent where ipaddress=\''+ipaddress+'\'  and tnsname=\''+tnsname+'\'  AND EVENT_NAME=\''+performance_type+'\'  order by sql_time desc'
        db = MySQLdb.connect("localhost","root","123456","oracle")
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        ddate=[]
        dtime=[]
        dweek=[]
        wait_time=[]
        total_timeouts=[]
        total_waits=[]
        format = '%Y-%m-%d %H:%M:%S'
        series_singal={}
        for j in result:
            if int(j[0]) >=int(starttime) and int(j[0])<=int(endtime):
                value= time.localtime(int(j[0]))
                dt = time.strftime(format, value).split()
                dt_week=dt[0].split('-')
                week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1]
                dweek.append(week)
                ddate.append(dt[0])
                dtime.append(dt[1])
                wait_time.append(int(j[1])/unit)
                total_timeouts.append(int(j[2]))
                total_waits.append(int(j[3]))
        result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'wait_time':wait_time,'total_timeouts':total_timeouts,'total_waits':total_waits})
        day_df=result.groupby('date')['total_timeouts','total_waits','wait_time'].first()-result.groupby('date')['total_timeouts','total_waits','wait_time'].last()
        #day_df['avg_wait']=(day_df['wait_time']/day_df['total_waits'])*1000
        series_singal['name']=ipaddress_tnsname
        series_singal['data']= day_df.total_waits.tolist()
        series_singal['x']=day_df.index.values.tolist()
        final_series.append(series_singal)
    return final_series
if __name__ == '__main__':
    performance_type='DBTime'
    ipaddress_tnsname_list=['10.65.1.119:DCPROD','10.65.1.172:ASEN']
    unit=60000000
    interval='day'
    starttime=1464710400
    endtime=1476201600
    print (oracle_performance_day(performance_type,ipaddress_tnsname_list,starttime,endtime,interval))
    #print oracle_performance_week(performance_type,ipaddress_tnsname_list,starttime,endtime,interval)
