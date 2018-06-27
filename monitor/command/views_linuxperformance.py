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
def linux_performance_day(performance_type,ipaddress_hostname_list,starttime,endtime,interval):
    final_series=[]
    x=[]
    #series_singal={}
    for starttime1 in range(starttime,endtime+1,86400):
        timearray=time.localtime(starttime1)
        x.append(time.strftime("%Y-%m-%d",timearray))
    #return x
    for ipaddress_hostname in ipaddress_hostname_list:
        key=performance_type+'='+ipaddress_hostname.split(':')[0]+'='+ipaddress_hostname.split(':')[1]
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
                dvalue.append(float(j[1]))
        result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'value':dvalue})
        day_df=result['value'].groupby(result['date'])
        day_result=day_df.mean()
        #return day_result
        series_reindex=pd.DataFrame({'date':day_result.index.values.tolist(),'value':day_result.values.tolist()})
        series_reindex.set_index('date',inplace=True)
        s=series_reindex.reindex(x,fill_value=series_reindex['value'].mean())
        series_singal['name']=ipaddress_hostname
        series_singal['data']= s['value'].values.tolist()
        series_singal['x']=s.index.values.tolist()
        final_series.append(series_singal)
    return final_series



if __name__ == '__main__':
    performance_type='CPU'
    ipaddress_hostname_list=['10.65.1.102:mes-db1']
    interval='day'
    starttime=1529856000
    endtime=1529942400
    print (linux_performance_day(performance_type,ipaddress_hostname_list,starttime,endtime,interval))
    #print oracle_performance_week(performance_type,ipaddress_tnsname_list,starttime,endtime,interval)
