#coding=utf8
from django.shortcuts import render
import MySQLdb
import cx_Oracle
import time
import datetime
from monitor.form import *
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpRequest
from django import template
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from monitor.models import *
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from monitor.command.views_getoraclecommandresult import *
from monitor.command.views_performance import *
from monitor.command.views_oracleperformance import *
from monitor.command.views_oracletopsql import *


def index(request):
    result=oraclelist.objects.all().order_by('tnsname')
    dic={'result':result}
    return render_to_response('index.html',dic)

def linux_list(request):
    result=linuxlist.objects.all().order_by('monitor_type')
    dic={'result':result}
    return render_to_response('linux_list.html',dic)

def oracle_command(request):
    result=oraclelist.objects.all().order_by('tnsname')
    dic={'result':result}
    return render_to_response('oracle_command.html',dic)


def commandresult(request):
    ipaddress  = str(request.GET['ipaddress']).split('-')[0]
    tnsname=str(request.GET['ipaddress']).split('-')[1]
    command_content  = str(request.GET['operate'])
    result=oraclelist.objects.all().order_by('tnsname')
    for i in result:
        if i.ipaddress==ipaddress:
            username =i.username
            password=i.password
            port=i.port
            break
    if command_content=='check_datafile_time':
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            cursor = db.cursor()
            row=getdatafilecreationtime(cursor)
            cursor.close()
            db.close()
            title='数据文件创建时间-'+ipaddress+'-'+tnsname
            tr=['数据文件名称','文件大小','表空间','自动扩展','创建时间']
            dic ={'title':title,'tr':tr,'row':row}
            #return render_to_response('oracle_command_result1.html',dic)
            html= render_to_string('oracle_command_result_5.html',dic)
            return HttpResponse(html)

    elif command_content=='check_analyzed_time':
        table_name1=[]
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            table_name  = str(request.GET['sql'])
            table_name=table_name.split()
            for i in table_name:
                table_name1.append('\''+str(i).strip().upper()+'\'')
            table_name=','.join(table_name1)
            cursor = db.cursor()
            row=getanalyzedtime(cursor,table_name)
            cursor.close()
            db.close()
            title='表分析的时间-'+ipaddress+'-'+tnsname
            tr=['OWNER','TABLE_NAME','NUM_ROWS','SAMPLE_SIZE','LAST_ANALYZED']
            dic ={'title':title,'tr':tr,'row':row}
            return render_to_response('oracle_command_result_5.html',dic)
    elif command_content=='check_segments_size':
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:

            cursor = db.cursor()
            row=getsegmentssize(cursor)
            cursor.close()
            db.close()
            title='数据库段的大小-'+ipaddress+'-'+tnsname
            tr=['OWNER','SEGMENTS_NAME','SEGMENTS_TYPE','TABLESPACE_NAME','BYTES/GB']
            dic ={'title':title,'tr':tr,'row':row}
            return render_to_response('oracle_command_result_5.html',dic)

    elif command_content=='check_process_text':
        pid1=[]
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            pid  = str(request.GET['sql'])
            pid=pid.split()
            for i in pid:
                pid1.append('\''+str(i).strip().upper()+'\'')
            pid=','.join(pid1)
            cursor = db.cursor()
            row=getprocesstext(cursor,pid)
            cursor.close()
            db.close()
            title='数据库进程对用的SQL语句-'+ipaddress+'-'+tnsname
            tr=['SPID','SID','HASH_VALUE','SQL_TEXT','LOGON_TIME','PROGRAM']
            dic ={'title':title,'tr':tr,'row':row}
            return render_to_response('oracle_command_result_6.html',dic)

    elif command_content=='check_session_process':
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            sid  = str(request.GET['sql'])
            cursor = db.cursor()
            row=getprocessno(cursor,sid)
            cursor.close()
            db.close()
            title='数据库进程号-'+ipaddress+'-'+tnsname+':'
            dic ={'title':title,'row':row}
            return render_to_response('oracle_command_result_1.html',dic)

    elif command_content=='check_temp_usage':
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            cursor = db.cursor()
            row=gettempusage(cursor)
            cursor.close()
            db.close()
            title=ipaddress+'-'+tnsname+' 数据库临时表空间使用率为: '
            dic ={'title':title,'row':row}
            return render_to_response('oracle_command_result_1.html',dic)

    elif command_content=='check_executions':
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            cursor = db.cursor()
            row=getexecutions(cursor)
            cursor.close()
            db.close()
            title='执行次数等于一语句-'+ipaddress+'-'+tnsname
            tr=['SQL语句','次数','模块']
            dic ={'title':title,'tr':tr,'row':row}
            return render_to_response('oracle_command_result_3.html',dic)

    elif command_content=='check_unboundsql':
        try:
            db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
        except Exception as  e:
            content= (ipaddress+' is Unreachable,The reason is '+ str(e)).strip()
            return HttpResponse(content)
        else:
            unboundsql  = str(request.GET['sql'])
            #return HttpResponse(unboundsql)
            cursor = db.cursor()
            row=getunboundsql(cursor,unboundsql)
            cursor.close()
            db.close()
            title='未绑定变量语句-'+ipaddress+'-'+tnsname
            tr=['SQL语句','哈希值','模块','第一次载入时间','上一次载入时间']
            dic ={'title':title,'tr':tr,'row':row}
            return render_to_response('oracle_command_result_5.html',dic)
def oracle_status(request):
    result=oraclestatus.objects.all().order_by('tnsname')
    dic ={'result':result}
    return render_to_response('oracle_status.html',dic)


def oracle_performance(request):
    baseline=[]
    ip=[]
    ip1=oraclelist.objects.all().order_by('ipaddress')
    for i in ip1:
        ip.append(i.ipaddress+':'+i.tnsname)
    if request.method == 'POST': # If the form has been submitted...
        #return HttpResponse('ss')
        form = charts_oracle_performance(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            starttime1  = request.POST['starttime']
            endtime1  = request.POST['endtime']
            performance_type= form.cleaned_data['performance_type']
            ipaddress_tnsname_list=form.cleaned_data['ipaddress']
            interval=request.POST['interval']
            if starttime1 =='' or endtime1 =='':
                return HttpResponse('Please give the Start and End time')
            else:
                starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d'))).split('.')[0])
                endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d'))).split('.')[0])
            if  starttime>endtime:
                return HttpResponse('The Start time must larger than the End time')
                #starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H:%M:%S'))))
                #endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H:%M:%S'))))
            else:
                    title='Oracle Performance '+'-'+performance_type
                    subtitle=performance_type
                    title_y=' Blocks/Seconds'
                    if performance_type in ['PhysicalReads','LogicalReads']:
                        unit='blocks/s'
                    elif performance_type in ['RedoSize']:
                        unit='bytes/s'
                    elif performance_type in ['DBTime','CPUTime']:
                        unit='Minites'
                    else:
                        unit='times/s'
                    final_series=[]
                    #final_series=oracle_performance_day(performance_type,ipaddress_tnsname_list,starttime,endtime,interval)
                    #return HttpResponse(final_series)
                    if interval=='day':
                        final_series=oracle_performance_day(performance_type,ipaddress_tnsname_list,starttime,endtime,interval)
                        x_categories=final_series[0]['x']
                    elif interval=='week':
                        final_series=oracle_performance_week(performance_type,ipaddress_tnsname_list,starttime,endtime,interval)
                        x_categories=final_series[0]['x']
                    #return HttpResponse(final_series)
                    dic={'categories':x_categories,'series':final_series,'title':title,'subtitle':subtitle,'unit':unit,'title_y':title_y}
                    #return render_to_response('highcharts_histogram.html',dic) # Redirect after POST
                    #return HttpResponse (final_series)
                    return render_to_response('highcharts.html',dic) # Redirect after POST
        else:
           return render(request, 'oracle_performance.html', {'form': form})
    else:
        form = charts_oracle_performance() # An unbound form
        d1=datetime.datetime.now()
        etime= d1.strftime("%Y%m%d")
        stime=(d1-datetime.timedelta(hours=720)).strftime("%Y%m%d")
        #etime= d1.strftime("%Y%m%d %H")
        #stime=(d1-datetime.timedelta(hours=24)).strftime("%Y%m%d %H")
        dic={'form':form,'etime':etime,'stime':stime}
        #dic={'form':form,'ip':ip,'ipaddress_checked':ipaddress_checked,'etime':etime,'stime':stime}
        return render(request, 'oracle_performance.html', dic)


def performance(request):
    baseline=[]
    ip=[]
    ip1=oraclelist.objects.all().order_by('ipaddress')
    for i in ip1:
        ip.append(i.ipaddress+':'+i.tnsname)
    if request.method == 'POST': # If the form has been submitted...
        form = charts_performance(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            starttime1  = request.POST['starttime']
            endtime1  = request.POST['endtime']
            ifcompare  = request.POST['ifcompare']
            performance_type= form.cleaned_data['performance_type']
            ipaddress_tnsname=form.cleaned_data['ipaddress']
#           return HttpResponse(ipaddress_tnsname)
            if starttime1 =='' or endtime1 =='':
                return HttpResponse('Please give the Start and End time')
            else:
                starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d'))).split('.')[0])
                endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d'))).split('.')[0])
            if  starttime>endtime:
                return HttpResponse('The Start time must larger than the End time')
                #starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H:%M:%S'))))
                #endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H:%M:%S'))))
            else:
                    title='Oracle Load Profile'+'-'+performance_type+'-'+ipaddress_tnsname
                    subtitle=ipaddress_tnsname
                    if performance_type in ['PhysicalReads','LogicalReads']:
                        unit='blocks/s'
                    elif performance_type in ['RedoSize']:
                        unit='bytes/s'
                    elif performance_type in ['DBTime','CPUTime']:
                        unit='Minites'
                    elif performance_type in ['MigrateRatio']:
                        unit='Percents'
                    else:
                        unit='times/s'
                    title_y=performance_type+' '+unit
                    x_categories=['01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00','24:00']
                    #x_categories=['01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00','23:59:59']
                    #x_categories=['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00','23:59:59']
                    final_series=[]
                    if performance_type=='MigrateRatio':
                        final_series=migrateratio_highcharts(performance_type,starttime,endtime,ipaddress_tnsname,ifcompare)
                    else:
                        final_series=loadprofile_highcharts(performance_type,starttime,endtime,ipaddress_tnsname,ifcompare)
                    #return HttpResponse(final_series)
                    dic={'categories':x_categories,'series':final_series,'title':title,'subtitle':subtitle,'unit':unit,'title_y':title_y}
                    #return render_to_response('highcharts_histogram.html',dic) # Redirect after POST
                    return render_to_response('highcharts_histogram.html',dic) # Redirect after POST
        else:
           return render(request, 'performance.html', {'form': form})
    else:
        form = charts_performance() # An unbound form
        d1=datetime.datetime.now()
        etime= d1.strftime("%Y%m%d")
        stime=(d1-datetime.timedelta(hours=72)).strftime("%Y%m%d")
        #etime= d1.strftime("%Y%m%d %H")
        #stime=(d1-datetime.timedelta(hours=24)).strftime("%Y%m%d %H")
        dic={'form':form,'etime':etime,'stime':stime}
        #dic={'form':form,'ip':ip,'ipaddress_checked':ipaddress_checked,'etime':etime,'stime':stime}
        return render(request, 'performance.html', dic)







def oracle_topevent(request):
    baseline=[]
    ip=[]
    ip1=oraclelist.objects.all().order_by('ipaddress')
    for i in ip1:
        ip.append(i.ipaddress+':'+i.tnsname)
    if request.method == 'POST': # If the form has been submitted...
        form = charts_oracle_topevent(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            starttime1  = request.POST['starttime']
            endtime1  = request.POST['endtime']
            performance_type= form.cleaned_data['performance_type']
            ipaddress_tnsname_list=form.cleaned_data['ipaddress']
            interval=request.POST['interval']
            wait=request.POST['wait']
#           return HttpResponse(ipaddress_tnsname)
            if starttime1 =='' or endtime1 =='':
                return HttpResponse('Please give the Start and End time')
            else:
                starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d'))).split('.')[0])
                endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d'))).split('.')[0])
            if  starttime>endtime:
                return HttpResponse('The Start time must larger than the End time')
                #starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H:%M:%S'))))
                #endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H:%M:%S'))))
            else:
                    title='Oracle Topevent '+'-'+performance_type
            starttime1  = request.POST['starttime']
            endtime1  = request.POST['endtime']
            performance_type= form.cleaned_data['performance_type']
            ipaddress_tnsname_list=form.cleaned_data['ipaddress']
            interval=request.POST['interval']
            wait=request.POST['wait']
#           return HttpResponse(ipaddress_tnsname)
            if starttime1 =='' or endtime1 =='':
                return HttpResponse('Please give the Start and End time')
            else:
                starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d'))).split('.')[0])
                endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d'))).split('.')[0])
            if  starttime>endtime:
                return HttpResponse('The Start time must larger than the End time')
                #starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H:%M:%S'))))
                #endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H:%M:%S'))))
            else:
                    title='Oracle Topevent '+'-'+performance_type
                    subtitle=performance_type
                    title_y=' Blocks/Seconds'
                    if wait=='total_waits':
                        unit='times'
                    else:
                        unit='ms'
                    final_series=[]
                    if interval=='day' and wait=='total_waits':
                        final_series=oracle_topevent_day_total_waits(performance_type,ipaddress_tnsname_list,starttime,endtime)
                        x_categories=final_series[0]['x']
                    elif interval=='day' and wait=='avg_wait':
                        final_series=oracle_topevent_day_avg_wait(performance_type,ipaddress_tnsname_list,starttime,endtime)
                        x_categories=final_series[0]['x']
                    elif interval=='hour' and wait=='total_waits':
                        final_series=oracle_topevent_hour_total_waits(performance_type,ipaddress_tnsname_list,starttime,endtime)
                        x_categories=['01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00','24:00']
                    elif interval=='hour' and wait=='avg_wait':
                        return HttpResponse('无此选项')
                    dic={'categories':x_categories,'series':final_series,'title':title,'subtitle':subtitle,'unit':unit,'title_y':title_y}
                    #return render_to_response('highcharts_histogram.html',dic) # Redirect after POST
                    #return HttpResponse (final_series)
                    return render_to_response('highcharts.html',dic) # Redirect after POST
        else:
           return render(request, 'oracle_topevent.html', {'form': form})
    else:
        form = charts_oracle_topevent() # An unbound form
        d1=datetime.datetime.now()
        etime= d1.strftime("%Y%m%d")
        stime=(d1-datetime.timedelta(hours=720)).strftime("%Y%m%d")
        #etime= d1.strftime("%Y%m%d %H")
        #stime=(d1-datetime.timedelta(hours=24)).strftime("%Y%m%d %H")
        dic={'form':form,'etime':etime,'stime':stime}
        #dic={'form':form,'ip':ip,'ipaddress_checked':ipaddress_checked,'etime':etime,'stime':stime}
        return render(request, 'oracle_topevent.html', dic)



def check_topsql(request):
    if request.method == 'POST': # If the form has been submitted...
        form = charts_topsql(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            top = form.cleaned_data['top']
            starttime1  = request.POST['starttime']
            endtime1  = request.POST['endtime']
            ipaddress = form.cleaned_data['ipaddress'].split(':')[0]
            tnsname = form.cleaned_data['ipaddress'].split(':')[1]
            topsql_type= form.cleaned_data['topsql_type'].split(':')[0]
            topsql_col=form.cleaned_data['topsql_type'].split(':')[1]
            title=tnsname+'-'+topsql_type+'-'+str(starttime1)+'-'+str(endtime1)

            if starttime1 =='' or endtime1 =='':
                return HttpResponse('Please give the Start and End time')
            else:
                starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H'))).split('.')[0])
                endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H'))).split('.')[0])+60
            if  starttime>endtime:
                return HttpResponse('The Start time must larger than the End time')
                #starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H:%M:%S'))))
                #endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H:%M:%S'))))
            else:
                    if  topsql_type=='diskreads':
                        row=check_topsql_diskreads(starttime,endtime,ipaddress,tnsname,topsql_type,top)
                    elif topsql_type=='buffergets':
                        row=check_topsql_buffergets(starttime,endtime,ipaddress,tnsname,topsql_type,top)
                    elif topsql_type=='elapsedtime':
                        row=check_topsql_elapsedtime(starttime,endtime,ipaddress,tnsname,topsql_type,top)
                    elif topsql_type=='cputime':
                        row=check_topsql_cputime(starttime,endtime,ipaddress,tnsname,topsql_type,top)
                    elif topsql_col=='topsegment':
                        row=check_topsql_topsegment(starttime,endtime,ipaddress,tnsname,topsql_type,top)
                    elif topsql_col=='segmentsizechange':
                        row=check_segmentsizechange(starttime,endtime,ipaddress,tnsname,topsql_type,top)
                    else:
                        row=check_topsql_topevent(starttime,endtime,ipaddress,tnsname,topsql_type,top)


                    top10sql=row['top10sql']
                    #outsql=row['outsql']
                    if topsql_type=='buffergets' or topsql_type=='diskreads':
                        tr=['SQL_ID','SQL 语句',topsql_type,'次数','数据块数/次','CPU时间(S)/次','时间(S)/次','模块']
                    elif topsql_type=='elapsedtime':
                        tr=['SQL_ID','SQL 语句',topsql_type,'次数','平均时间(S)','CPU时间(S)/次','模块']
                    elif topsql_type=='cputime':
                        tr=['SQL_ID','SQL 语句',topsql_type,'次数','平均CPU时间(S)','执行时间(S)/次','模块']
                    elif topsql_col=='topsegment':
                        tr=['用户','对象名','分区名','对象类型','值']
                    elif topsql_col=='segmentsizechange':
                        tr=['用户','对象名','分区名','对象类型','表空间','大小/M','大小变化量/M','块变化量/Blocks','每天大小变化量/M']
                    else:
                        tr=['事件名称','等待时间','等待次数','平均等待时间','等待超时次数']
                    #dic ={'title':title,'tr':tr,'top10sql':top10sql,'outsql':outsql}
                    dic ={'title':title,'tr':tr,'top10sql':top10sql}
                    if topsql_type=='buffergets' or topsql_type=='diskreads':
                        return render_to_response('oracle_topsql_8.html',dic)
                    elif topsql_type=='elapsedtime' or topsql_type=='cputime':
                        return render_to_response('oracle_topsql_7.html',dic)
                    elif topsql_type=='topevent':
                        return render_to_response('oracle_topsql_5.html',dic)



        else:
           return render(request, 'check_topsql.html', {'form': form})
    else:
        form = charts_topsql() # An unbound form
        d1=datetime.datetime.now()
        etime= d1.strftime("%Y%m%d %H")
        stime=(d1-datetime.timedelta(hours=1)).strftime("%Y%m%d %H")
        dic={'form':form,'etime':etime,'stime':stime}
        return render(request, 'check_topsql.html', dic)









def addbaseline(request):
    r=redis.StrictRedis()
    if request.method=='POST':
        form=charts_addbaseline(request.POST)
        if form.is_valid(): # All validation rules pass
            baselinetime  = request.POST['baselinetime']
            #performance_type= form.cleaned_data['performance_type']
            ipaddress_tnsname=form.cleaned_data['ipaddress']
            #return HttpResponse(performance_type)

            if baselinetime =='':
                return HttpResponse('Please give the Baseline Time')
            else:
                baselinetime=int(str(time.mktime(time.strptime(baselinetime,'%Y%m%d'))).split('.')[0])
            ptype=['PhysicalReads','LogicalReads','HardParse','TotalParse','UserCommits','UserRollbacks','Logons','SortsDisk','UserCalls','RedoSize','ExecuteCount','DBTime']
            for performance_type in ptype:
                for i in r.keys():
                    monitor=i.split('=')[1]+':'+i.split('=')[2]
                    if i.split('=')[0]==performance_type and monitor == ipaddress_tnsname:
                        value1=[]
                        value2=[]
                        for k in range(0,len(r.lrange(i,start=0,end=-1))):
                                value=r.lindex(i,k).split(':')
                                if baselinetime+300+86400>=int(value[0])>=baselinetime:
                                    value1.append(int(value[1]))
                        if performance_type=='DBTime':
                            value1.reverse()
                            #return HttpResponse(value1)
                            for n in range(0,len(value1)-1):
                                diff=(value1[n+1]-value1[n])/60/1000000
                                value2.append(diff)
                        elif performance_type=='SortsDisk':
                            value1.reverse()
                            #return HttpResponse(value1)
                            for n in range(0,len(value1)-1):
                                diff=(value1[n+1]-value1[n])
                                value2.append(diff)
                        else:
                            value1.reverse()
                            #return HttpResponse(value1)
                            for n in range(0,len(value1)-1):
                                diff=(value1[n+1]-value1[n])/3600
                                value2.append(diff)
                baselinekey=performance_type+'Baseline='+ipaddress_tnsname.split(':')[0]+'='+ipaddress_tnsname.split(':')[1]
                baselinevalue=value2
                r.set(baselinekey,baselinevalue)
            return HttpResponse('Add Sucessful')
    else:
        form = charts_addbaseline() # An unbound form
        d1=datetime.datetime.now()
        etime= d1.strftime("%Y%m%d")
        #etime= d1.strftime("%Y%m%d %H")
        #stime=(d1-datetime.timedelta(hours=24)).strftime("%Y%m%d %H")
        dic={'form':form,'etime':etime}
        #dic={'form':form,'ip':ip,'ipaddress_checked':ipaddress_checked,'etime':etime,'stime':stime}
        return render(request, 'addbaseline.html', dic)


def check_hitratio(request):
    ip=[]
    ip1=oraclelist.objects.all().order_by('ipaddress')
    for i in ip1:
        ip.append(i.ipaddress+':'+i.tnsname)
    if request.method == 'POST': # If the form has been submitted...
        form = charts_hitratio(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            ipaddress_tnsname=[]
            ipaddress1=request.REQUEST.getlist('hitratio')
            for i in ipaddress1:
                ipaddress_tnsname.append(i)
            starttime1  = request.POST['starttime']
            endtime1  = request.POST['endtime']
            count = form.cleaned_data['granularity']
            ratio_type= form.cleaned_data['ratio_type']
            if starttime1 =='' or endtime1 =='':
                return HttpResponse('Please give the Start and End time')
            else:
                starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H'))).split('.')[0])
                endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H'))).split('.')[0])
            if  starttime>endtime:
                return HttpResponse('The Start time must larger than the End time')
                #starttime=int(str(time.mktime(time.strptime(starttime1,'%Y%m%d %H:%M:%S'))))
                #endtime=int(str(time.mktime(time.strptime(endtime1,'%Y%m%d %H:%M:%S'))))
            else:
                    title='Oracle Hit Ratio '+'-'+ratio_type
                    title_y='Ratio Percents'
                    x_categories=[]
                    final_series=[]
                    for categories in range (starttime,endtime+count*3600,count*3600):
                    #for categories in range (starttime,endtime,count*3600):
                        categories=time.localtime(categories)
                        interval= strf_local_time=time.strftime('%m/%d %H',categories)
                        x_categories.append(interval)
                    final_series=hitratio_highcharts(x_categories,ratio_type,starttime,endtime,count,ipaddress_tnsname)
                    dic={'categories':x_categories,'series':final_series,'title':title,'title_y':title_y}
                    return render_to_response('highcharts.html',dic) # Redirect after POST
        else:
           return render(request, 'check_graphic.html', {'form': form})
    else:
        form = charts_hitratio() # An unbound form
        ipaddress_checked=[]
        ipaddress_check=['10.65.1.203','10.65.1.118','10.60.14.70','10.65.1.119','10.65.1.113','10.65.1.109','10.65.1.110']
        for i in ip1:
            if i.ipaddress in ipaddress_check:
                ipaddress_checked.append(i.ipaddress+':'+i.tnsname)
        d1=datetime.datetime.now()
        etime= d1.strftime("%Y%m%d %H")
        stime=(d1-datetime.timedelta(hours=24)).strftime("%Y%m%d %H")
        dic={'form':form,'ip':ip,'ipaddress_checked':ipaddress_checked,'etime':etime,'stime':stime}
        return render(request, 'check_hitratio.html', dic)
