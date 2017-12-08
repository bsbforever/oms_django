#!/usr/bin/python
#coding=utf-8
import redis
import time
import pandas as pd
import datetime
import MySQLdb
from django.http import HttpResponse
from django.http import HttpRequest
def space_highcharts(x_categories,starttime,endtime,count,ipaddress):
    r=redis.StrictRedis()
    final_series=[]
    for i in r.keys():
        if i.split('=')[0]=='Diskspace' and i.split('=')[1]==ipaddress:
            all_value={}
            series_value=[]
            series_singal={}
            interval_value=[]
            final_value2=[]
    #check  one more time that belong to same time interval.
        for k in range(0,len(r.lrange(i,start=0,end=-1))):
            value1=[]
            value=r.lindex(i,k).split(':')
            if int(endtime)+300>=int(value[0])>=int(starttime):
                time1=int(value[0])
                local_time=time.localtime(time1)
                strf_local_time=time.strftime('%m/%d %H',local_time)
             #strf_local_time=time.strftime('%m/%d',local_time)
                if all_value.has_key(strf_local_time):
                    value1.append(int(value[1]))
                    all_value[strf_local_time]=value1
                else:
                    del value1[:]
                    value1.append(int(value[1]))
                    all_value[strf_local_time]=value1
            else:
                if int(value[0]) <starttime:
                    break
                else:
                    continue
            #return HttpResponse(all_value.items())
        for a in x_categories:
            if a  in all_value.keys():
                pass
            else:
                all_value[a]=[0]
         #return HttpResponse(all_value.keys())
        #calculate the avg result between one hours
        result=sorted(all_value.items(),key=lambda all_value:all_value[0])
    for key in result:
        #x_categories.append(key[0])
        l=0
        for n in key[1]:
            l=l+n
        final_value=l/len(key[1])
        series_value.append(final_value)
            #return HttpResponse(len(series_value))
        #calculate the avg. result while the calculate is larger than 1 hour
    for p in range(0,len(series_value),count):
        interval_value1=series_value[p:p+count]
        interval_value.append(interval_value1)
        #return HttpResponse(interval_value)
    for q in interval_value:
        x=0
        for y in q:
            x=x+y
        final_value1=x/len(q)
        final_value2.append(final_value1)
    series_singal['name']=i.split('=')[3]
    series_singal['data']=final_value2
    final_series.append(series_singal)
    return final_series

def cpumem_highcharts(x_categories,os_performance,starttime,endtime,count,ipaddress_hostname):
    r=redis.StrictRedis()
    final_series=[]
    for i in r.keys():
        monitor= i.split('=')[1]+':'+i.split('=')[2]
        if i.split('=')[0]==os_performance and monitor in ipaddress_hostname:
            all_value={}
            series_value=[]
            series_singal={}
            interval_value=[]
            final_value2=[]
        #check  one more time that belong to same time interval.
            for k in range(0,len(r.lrange(i,start=0,end=-1))):
                value1=[]
                value=r.lindex(i,k).split(':')
                if int(endtime)+300>=int(value[0])>=int(starttime):
                    time1=int(value[0])
                    local_time=time.localtime(time1)
                    strf_local_time=time.strftime('%m/%d %H:%M',local_time)
                    #strf_local_time=time.strftime('%m/%d',local_time)
                    if all_value.has_key(strf_local_time):
                        value1.append(float(value[1]))
                        all_value[strf_local_time]=value1
                    else:
                        del value1[:]
                        value1.append(float(value[1]))
                        all_value[strf_local_time]=value1

                else:
                    if int(value[0]) <starttime:
                        break
                    else:
                        continue
            #return HttpResponse(all_value.items())
            for a in x_categories:
                if a  in all_value.keys():
                    pass
                else:
                    all_value[a]=[0]
            #return HttpResponse(all_value.keys())
        #calculate the avg result between one hours
            result=sorted(all_value.items(),key=lambda all_value:all_value[0])
            for key in result:
    #               x_categories.append(key[0])
                l=0
                for n in key[1]:
                    l=l+n
                final_value=l/len(key[1])
                series_value.append(final_value)
            #return HttpResponse(len(series_value))
        #calculate the avg. result while the calculate is larger than 1 hour
            for p in range(0,len(series_value),count):
                interval_value1=series_value[p:p+count]
                interval_value.append(interval_value1)
                #return HttpResponse(interval_value)
            for q in interval_value:
                x=0
                for y in q:
                    x=x+y
                final_value1=x/len(q)
                final_value2.append(final_value1)
            series_singal['name']=i.split('=')[1]+'-'+i.split('=')[2]
            series_singal['data']=final_value2
            final_series.append(series_singal)
    return final_series
def hitratio_highcharts(x_categories,ratio_type,starttime,endtime,count,ipaddress_tnsname):
    r=redis.StrictRedis()
    final_series=[]
    for i in r.keys():
        monitor=i.split('=')[1]+':'+i.split('=')[2]
        if i.split('=')[0]==ratio_type and monitor  in ipaddress_tnsname:
            all_value={}
            series_value=[]
            series_singal={}
            interval_value=[]
            final_value2=[]
        #check  one more time that belong to same time interval.
            for k in range(0,len(r.lrange(i,start=0,end=-1))):
                value1=[]
                value=r.lindex(i,k).split(':')
                if int(endtime)+300>=int(value[0])>=int(starttime):
                    time1=int(value[0])
                    local_time=time.localtime(time1)
                    strf_local_time=time.strftime('%m/%d %H',local_time)
                    #strf_local_time=time.strftime('%m/%d',local_time)
                    if all_value.has_key(strf_local_time):
                        value1.append(float(value[1]))
                        all_value[strf_local_time]=value1
                    else:
                        del value1[:]
                        value1.append(float(value[1]))
                        all_value[strf_local_time]=value1

            else:
                if int(value[0]) <starttime:
                    break
                else:
                    continue
            #return HttpResponse(all_value.items())
            for a in x_categories:
                if a  in all_value.keys():
                    pass
                else:
                    all_value[a]=[0]
                   #return HttpResponse(all_value.keys())
        #calculate the avg result between one hours
            result=sorted(all_value.items(),key=lambda all_value:all_value[0])
            for key in result:
    #           x_categories.append(key[0])
                l=0
                for n in key[1]:
                    l=l+n
                final_value=l/len(key[1])
                series_value.append(final_value)
                #return HttpResponse(len(series_value))
        #calculate the avg. result while the calculate is larger than 1 hour
            for p in range(0,len(series_value),count):
                interval_value1=series_value[p:p+count]
                interval_value.append(interval_value1)
                #return HttpResponse(interval_value)
            for q in interval_value:
                x=0
                for y in q:
                    x=x+y
                final_value1=x/len(q)
                final_value2.append(final_value1)
            series_singal['name']=i.split('=')[0]+'-'+i.split('=')[1]+'-'+i.split('=')[2]
            series_singal['data']=final_value2
            final_series.append(series_singal)
    return final_series


def loadprofile_highcharts(performance_type,starttime,endtime,ipaddress_tnsname,ifcompare):
    final_series=[]
    r=redis.StrictRedis()
    if performance_type in ['LogicalReads','PhysicalReads']:
        unit=3600
    elif performance_type=='DBTime':
        unit=60000000
    elif performance_type in ['SortsDisk','FetchContinuedRow','FetchByRowid']:
        unit=24
    elif performance_type =='CPUTime':
        unit=6000
    else:
        unit=3600

    key=performance_type+'='+ipaddress_tnsname.split(':')[0]+'='+ipaddress_tnsname.split(':')[1] 
    format = '%Y-%m-%d %H:%M:%S'
    ddate=[]
    dtime=[]
    dvalue=[]
    dweek=[]
    final_series=[]
    result=r.lrange(key,0,3600)
    for i in result:
        j=i.decode().split(':') #b'1511157600:175548353'
        #return j[1]
        if int(j[0]) >=starttime and int(j[0])<endtime+86400:
            value1= time.localtime(int(j[0])) #time.struct_time(tm_year=2017, tm_mon=11, tm_mday=19, tm_hour=14
            dt = time.strftime(format, value1).split() # before split format 2017-11-19 14:21:03
            dt_week=dt[0].split('-')
            week=datetime.date(int(dt_week[0]),int(dt_week[1]),int(dt_week[2])).isocalendar()[1]  #caculate datte's week
            dweek.append(week)
            ddate.append(dt[0])
            dtime.append(dt[1])
            dvalue.append(int(j[1])/unit)
            #return dvalue
            #print (week)
    result=pd.DataFrame({'week':dweek,'date':ddate,'time':dtime,'value':dvalue})
    new_index=['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00','23:59:59']


    #day_df=result['time'],['value'].groupby(result['date'])
    day_df=result.groupby(result['date'])
    for name,group in day_df:
        series_singal={}
        flist1=[]
        #print (name)
        group.set_index('time',inplace=True)
        s=group.reindex(new_index,fill_value=group['value'].mean())
        series_singal['name']=name
        flist= s['value'].values.tolist()
        j=flist[1:]
        k=flist[0:-1]
        for i in range(0,len(j)):
            flist1.append(j[i]-k[i])
        series_singal['data']= flist1
        final_series.append(series_singal)
    #print (final_series)
    #break
            
    if ifcompare=='yes':
        for i in r.keys():
            monitor=i.split('=')[1]+':'+i.split('=')[2]
            #return HttpResponse(monitor)
            baseline_dic={}
            if i.split('=')[0]==performance_type+'Baseline' and monitor == ipaddress_tnsname:
                baselinevalue=r.get(i)
                baseline_dic['name']='Baseline'
                baseline_dic['data']=baselinevalue
                final_series.append(baseline_dic)
    return final_series


def migrateratio_highcharts(performance_type,baseline,ipaddress_tnsname,ifcompare):
    r=redis.StrictRedis()
    final_series=[]
    for date in baseline:
        for i in r.keys():
            monitor=i.split('=')[1]+':'+i.split('=')[2]
            series_singal={}
            value3=[]
            if i.split('=')[0]=='FetchContinuedRow' and monitor == ipaddress_tnsname:
                timearray=time.strptime(date,"%Y-%m-%d")
                date1=int(str(time.mktime(timearray)).split('.')[0])
                value1=[]
                FetchContinuedRow=[]
                for k in range(0,len(r.lrange(i,start=0,end=-1))):
                    value=r.lindex(i,k).split(':')
                    if date1+300+86400>=int(value[0])>=date1:
                        value1.append(int(value[1]))
                value1.reverse()
            #return HttpResponse(value1)
                for n in range(0,len(value1)-1):
                    diff=value1[n+1]-value1[n]
                    FetchContinuedRow.append(diff)
            if i.split('=')[0]=='FetchByRowid' and monitor == ipaddress_tnsname:
                timearray=time.strptime(date,"%Y-%m-%d")
                date1=int(str(time.mktime(timearray)).split('.')[0])
                value1=[]
                FetchByRowid=[]
                for k in range(0,len(r.lrange(i,start=0,end=-1))):
                    value=r.lindex(i,k).split(':')
                    if date1+300+86400>=int(value[0])>=date1:
                        value1.append(int(value[1]))
                value1.reverse()
                #return HttpResponse(value1)
                for n in range(0,len(value1)-1):
                    diff= value1[n+1]-value1[n]
                    FetchByRowid.append(diff)
                #return HttpResponse(value2)
        for k in range(0,24):
            value3.append(float(FetchContinuedRow[k])/float(FetchByRowid[k])*100)
        series_singal['name']=date
        series_singal['data']=value3
        final_series.append(series_singal)
    if ifcompare=='yes':
        for i in r.keys():
            monitor=i.split('=')[1]+':'+i.split('=')[2]
            #return HttpResponse(monitor)
            baseline_dic={}
            if i.split('=')[0]==performance_type+'Baseline' and monitor == ipaddress_tnsname:
                baselinevalue=r.get(i)
                baseline_dic['name']='Baseline'
                baseline_dic['data']=baselinevalue
                final_series.append(baseline_dic)
    return final_series

def performance_highcharts(x_categories,performance_type,count,starttime,endtime,ipaddress_tnsname):
    col_name=performance_type.split(':')[1]
    table_name=performance_type.split(':')[0]
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='oracle',port=3306)
    cur=conn.cursor()
    final_series=[]
    for i in ipaddress_tnsname:
        ipaddress=i.split(':')[0]
        tnsname=i.split(':')[1]
        getsql_text='select sql_time,sum('+col_name+') from oracle_oracle_'+table_name+' where sql_time>='+str(starttime)+' and sql_time<='+str(endtime+60)+' and ipaddress=\''+ipaddress+'\' and tnsname=\''+tnsname+'\' group by sql_time order by sql_time'
        cur.execute(getsql_text)
        row=cur.fetchall()
        result={}
        data=[]
        data1=[]
        final_data=[]
        final_single={}
        for l in row:
            time1=time.localtime(l[0])
            interval= strf_local_time=time.strftime('%m/%d %H',time1)
            result[interval]=l[1]
        for j in x_categories:
            if j in result.keys():
                pass
            else:
                result[j]=0
        result1=sorted(result.items(),key=lambda result:result[0])
        for k in result1:
            data.append(int(k[1]))
        for  x   in range(0,len(data),count):
            data1.append(data[x:x+count])
        for  y in data1:
            h=0
            for z in y:
                h=h+z
            final_data.append(h/len(y)) 
        
            
        final_single['name']=table_name+'-'+ipaddress+'-'+tnsname
        final_single['data']=final_data
        final_series.append(final_single)
    cur.close()
    conn.close()
    return final_series
