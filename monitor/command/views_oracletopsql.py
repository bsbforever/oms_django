import re
import os
import time
import datetime
import MySQLdb
import pandas as pd
def check_segmentsizechange(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    hour=0
    result={}
    for i in range(starttime,endtime,86400):
        hour=hour+1
    topsql=[]
    top10sql=[]
    outsql=[]
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='oracle',port=3306)
    cur=conn.cursor()
    getsql_text='select * from oracle_segmentsizechange where segment_time <='+ str(endtime)+' and segment_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by ipaddress,tnsname,OWNER,segment_name,	partition_name,segment_type,segment_time'
    cur.execute(getsql_text)
    row=cur.fetchall()
    cur.close()
    conn.close()
    count=hour
    sql_id='sql_id'
    for i in row:
        if i[6] is None:
            name=i[4]+'_'+i[5]+'_'+i[7]+'_'+i[8]
        else:
            name=i[4]+'_'+i[5]+'_'+i[6]+'_'+i[7]+'_'+i[8]
        if name==sql_id:
            count=count+1
            if count==hour:
                maxtime=i
                owner=maxtime[4]
                segment_name=maxtime[5]
                patition_name=maxtime[6]
                segment_type=maxtime[7]
                tablespace_name=maxtime[8]
                segment_bytes=maxtime[9]/1024/1024
                byteschange=(maxtime[9]-mintime[9])/1024/1024
                byteschangeperday=byteschange/(hour-1)
                blockschange=maxtime[10]-mintime[10]
                topsql.append([owner,segment_name,patition_name,segment_type,tablespace_name,segment_bytes,byteschange,blockschange,byteschangeperday])
        else:
            if count!=hour and sql_id !='sql_id':
                outsql1=str(mintime[4])+'-'+str(mintime[5])+' is wrapped out '+str(hour-count)+' times'
                outsql.append(outsql1)
            mintime=i
            count=1
            if i[6] is None:
                sql_id=i[4]+'_'+i[5]+'_'+i[7]+'_'+i[8]
            else:
                sql_id=i[4]+'_'+i[5]+'_'+i[6]+'_'+i[7]+'_'+i[8]

    if topsql_type=='elapsedtime':
        topsql.sort(key=lambda x:x[6],reverse=True)
    else:
        topsql.sort(key=lambda x:x[6],reverse=True)
    for n in range(0,top if len(topsql)>=top else len(topsql)):
        top10sql.append(topsql[n])
    result['top10sql']=top10sql
    if len(outsql)!=0:
        result['outsql']=outsql
    else:
        result['outsql']=[]
    return result
def check_topsql_topsegment(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    hour=0
    result={}
    for i in range(starttime,endtime,3600):
        hour=hour+1
    topsql=[]
    top10sql=[]
    outsql=[]
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='oracle',port=3306)
    cur=conn.cursor()
    getsql_text='select * from oracle_topsegment where statistic_name=\"'+topsql_type+'\" and sql_time <='+ str(endtime)+' and sql_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by object_name,sql_time'
    cur.execute(getsql_text)
    row=cur.fetchall()
    cur.close()
    conn.close()
    count=hour
    sql_id='sql_id'
    for i in row:
        if i[4]==sql_id:
            count=count+1
            if count==hour:
                maxtime=i
                owner=maxtime[4].split('_')[0]
                object_name=maxtime[4].split('.')[0].split('_')[1:len(maxtime[4].split('.')[0].split('_'))-1]
                subobject_name=maxtime[4].split('.')[1]
                object_name='_'.join(object_name)
                #object_name=maxtime[4]
                object_type=maxtime[4].split('.')[0].split('_')[-1]
                value=maxtime[6]-mintime[6]
                if value<0:
                    value=maxtime[6]
                else:
                    pass
                topsql.append([owner,object_name,subobject_name,object_type,value])
        else:
            if count!=hour and sql_id !='sql_id':
                outsql1=str(mintime[4])+'-'+str(mintime[5])+' is wrapped out '+str(hour-count)+' times'
                outsql.append(outsql1)
            mintime=i
            count=1
            sql_id=i[4]

    if topsql_type=='elapsedtime':
        topsql.sort(key=lambda x:x[6],reverse=True)
    else:
        topsql.sort(key=lambda x:x[4],reverse=True)
    for n in range(0,top if len(topsql)>=top else len(topsql)):
        top10sql.append(topsql[n])
    result['top10sql']=top10sql
    if len(outsql)!=0:
        result['outsql']=outsql
    else:
        result['outsql']=[]
    return result



def check_topsql_diskreads(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    result={}
    conn=MySQLdb.connect(host='localhost',user='oracle',passwd='dgvtG@ng1',db='oracle',port=3306)
    getsql_text='select * from monitor_oracle_'+topsql_type+' where sql_time <='+ str(endtime)+' and sql_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by sql_id ,sql_time desc'
    df = pd.read_sql(getsql_text, con=conn)
    conn.close()
    sql_id_group=df.groupby('sql_id') #以SQL_ID为进行分组
    sql_id_list=[]
    disk_reads_list=[]
    executions_list=[]
    disk_reads_per_list=[]
    cpu_time_list=[]
    elapsed_time_list=[]
    module_list=[]
    sql_text_list=[]
    for name1,group1 in sql_id_group: ##迭代各个分组 
        sql_id=name1
        #计算各个分组不同性能指标的差值,第一个减去最后一个
        disk_reads= (group1['disk_reads'].values[0]-group1['disk_reads'].values[-1])
        executions = int((group1['executions'].values[0] - group1['executions'].values[-1]))
        if executions==0: #若执行次数为0，则将分母变为1
            executions_after=1
        else:
            executions_after=executions
        disk_reads_per = round(int((group1['disk_reads'].values[0]-group1['disk_reads'].values[-1]))/executions_after,2)
        cpu_time= round(int((group1['cpu_time'].values[0] - group1['cpu_time'].values[-1]))/1000000/executions_after,2)
        elapsed_time = round(int((group1['elapsed_time'].values[0] - group1['elapsed_time'].values[-1]))/1000000/executions_after,1)
        module=group1['module'].values[0]
        sql_text = group1['sql_text'].values[0]
        sql_id_list.append(sql_id)
        disk_reads_list.append(disk_reads)
        executions_list.append(executions)
        disk_reads_per_list.append(disk_reads_per)
        cpu_time_list.append(cpu_time)
        elapsed_time_list.append(elapsed_time)
        module_list.append(module)
        sql_text_list.append(sql_text)
    #将整理后的数据格式化成DataFrame格式,并按照一定顺序排列
    columns=['sql_id','sql_text','disk_reads','executions','disk_reads_per','cpu_time','elapsed_time','module']
    topsql=pd.DataFrame({'sql_id':sql_id_list,'sql_text':sql_text_list,'disk_reads':disk_reads_list,'executions':executions_list,'disk_reads_per':disk_reads_per_list,'cpu_time':cpu_time_list,'elapsed_time':elapsed_time_list,'module':module_list},columns=columns)
    # 利用pandas排序函数以disk_reads的值来降序排列，得到TOP语句
    top10=topsql.sort_values(by=['disk_reads'], ascending=False).head(top).values
    result['top10sql']=top10
    return (result)



def check_topsql_buffergets(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    result={}
    conn=MySQLdb.connect(host='localhost',user='oracle',passwd='dgvtG@ng1',db='oracle',port=3306)
    getsql_text='select * from monitor_oracle_'+topsql_type+' where sql_time <='+ str(endtime)+' and sql_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by sql_id ,sql_time desc'
    df = pd.read_sql(getsql_text, con=conn)
    conn.close()
    sql_id_group=df.groupby('sql_id')
    sql_id_list=[]
    buffer_gets_list=[]
    executions_list=[]
    buffer_gets_per_list=[]
    cpu_time_list=[]
    elapsed_time_list=[]
    module_list=[]
    sql_text_list=[]
    for name1,group1 in sql_id_group:
        sql_id=name1
        buffer_gets= (group1['buffer_gets'].values[0]-group1['buffer_gets'].values[-1])
        executions = int((group1['executions'].values[0] - group1['executions'].values[-1]))
        if executions==0:
            executions_after=1
        else:
            executions_after=executions
        buffer_gets_per = round(int((group1['buffer_gets'].values[0]-group1['buffer_gets'].values[-1]))/executions_after,2)
        cpu_time= round(int((group1['cpu_time'].values[0] - group1['cpu_time'].values[-1]))/1000000/executions_after,2)
        elapsed_time = round(int((group1['elapsed_time'].values[0] - group1['elapsed_time'].values[-1]))/1000000/executions_after,1)
        module=group1['module'].values[0]
        sql_text = group1['sql_text'].values[0]
        sql_id_list.append(sql_id)
        buffer_gets_list.append(buffer_gets)
        executions_list.append(executions)
        buffer_gets_per_list.append(buffer_gets_per)
        cpu_time_list.append(cpu_time)
        elapsed_time_list.append(elapsed_time)
        module_list.append(module)
        sql_text_list.append(sql_text)
    columns=['sql_id','sql_text','buffer_gets','executions','buffer_gets_per','cpu_time','elapsed_time','module']
    topsql=pd.DataFrame({'sql_id':sql_id_list,'sql_text':sql_text_list,'buffer_gets':buffer_gets_list,'executions':executions_list,'buffer_gets_per':buffer_gets_per_list,'cpu_time':cpu_time_list,'elapsed_time':elapsed_time_list,'module':module_list},columns=columns)
    top10=topsql.sort_values(by=['buffer_gets'], ascending=False).head(top).values
    result['top10sql']=top10
    return (result)



def check_topsql_elapsedtime(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    result={}
    conn=MySQLdb.connect(host='localhost',user='oracle',passwd='dgvtG@ng1',db='oracle',port=3306)
    getsql_text='select * from monitor_oracle_'+topsql_type+' where sql_time <='+ str(endtime)+' and sql_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by sql_id ,sql_time desc'
    df = pd.read_sql(getsql_text, con=conn)
    conn.close()
    sql_id_group=df.groupby('sql_id')
    sql_id_list=[]
    elapsed_time_list=[]
    executions_list=[]
    cpu_time_list=[]
    elapsed_time_per_list=[]
    module_list=[]
    sql_text_list=[]
    for name1,group1 in sql_id_group:
        sql_id=name1
        elapsed_time = round(int((group1['elapsed_time'].values[0] - group1['elapsed_time'].values[-1])) / 1000000,1)
        executions = int((group1['executions'].values[0] - group1['executions'].values[-1]))
        if executions==0:
            executions_after=1
        else:
            executions_after=executions
        cpu_time= round(int((group1['cpu_time'].values[0] - group1['cpu_time'].values[-1]))/1000000/executions_after,2)
        elapsed_time_per = round(int((group1['elapsed_time'].values[0] - group1['elapsed_time'].values[-1]))/1000000/executions_after,1)
        module=group1['module'].values[0]
        sql_text = group1['sql_text'].values[0]
        sql_id_list.append(sql_id)
        elapsed_time_list.append(elapsed_time)
        elapsed_time_per_list.append(elapsed_time_per)
        executions_list.append(executions)
        cpu_time_list.append(cpu_time)
        module_list.append(module)
        sql_text_list.append(sql_text)
    columns=['sql_id','sql_text','elapsed_time','executions','elapsed_time_per','cpu_time','module']
    topsql=pd.DataFrame({'sql_id':sql_id_list,'sql_text':sql_text_list,'elapsed_time':elapsed_time_list,'executions':executions_list,'elapsed_time_per':elapsed_time_per_list,'cpu_time':cpu_time_list,'module':module_list},columns=columns)
    top10=topsql.sort_values(by=['elapsed_time'], ascending=False).head(top).values
    result['top10sql']=top10
    return (result)




def check_topsql_cputime(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    result={}
    conn=MySQLdb.connect(host='localhost',user='oracle',passwd='dgvtG@ng1',db='oracle',port=3306)
    getsql_text='select * from monitor_oracle_'+topsql_type+' where sql_time <='+ str(endtime)+' and sql_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by sql_id ,sql_time desc'
    df = pd.read_sql(getsql_text, con=conn)
    conn.close()
    sql_id_group=df.groupby('sql_id')
    sql_id_list=[]
    elapsed_time_list=[]
    executions_list=[]
    cpu_time_list=[]
    cpu_time_per_list=[]
    module_list=[]
    sql_text_list=[]
    for name1,group1 in sql_id_group:
        sql_id=name1
        cpu_time= round(int((group1['cpu_time'].values[0] - group1['cpu_time'].values[-1]))/1000000,2)
        executions = int((group1['executions'].values[0] - group1['executions'].values[-1]))
        if executions==0:
            executions_after=1
        else:
            executions_after=executions
        cpu_time_per= round(int((group1['cpu_time'].values[0] - group1['cpu_time'].values[-1]))/1000000/executions_after,2)
        elapsed_time = round(int((group1['elapsed_time'].values[0] - group1['elapsed_time'].values[-1]))/1000000/executions_after,1)
        module=group1['module'].values[0]
        sql_text = group1['sql_text'].values[0]
        sql_id_list.append(sql_id)
        elapsed_time_list.append(elapsed_time)
        cpu_time_per_list.append(cpu_time_per)
        executions_list.append(executions)
        cpu_time_list.append(cpu_time)
        module_list.append(module)
        sql_text_list.append(sql_text)
    columns=['sql_id','sql_text','cpu_time','executions','cpu_time_per','elapsed_time','module']
    topsql=pd.DataFrame({'sql_id':sql_id_list,'sql_text':sql_text_list,'cpu_time':cpu_time_list,'executions':executions_list,'cpu_time_per':cpu_time_per_list,'elapsed_time':elapsed_time_list,'module':module_list},columns=columns)
    top10=topsql.sort_values(by=['cpu_time'], ascending=False).head(top).values
    result['top10sql']=top10
    return (result)





def check_topsql_topevent(starttime,endtime,ipaddress,tnsname,topsql_type,top):
    result={}
    conn=MySQLdb.connect(host='localhost',user='oracle',passwd='dgvtG@ng1',db='oracle',port=3306)
    getsql_text='select * from monitor_oracle_'+topsql_type+' where sql_time <='+ str(endtime)+' and sql_time >='+str(starttime)+' and tnsname=\''+tnsname+'\' and ipaddress=\''+ipaddress+'\' order by event_name ,sql_time desc'
    df = pd.read_sql(getsql_text, con=conn)
    conn.close()
    event_name_group=df.groupby('event_name')
    event_name_list=[]
    total_waits_list=[]
    total_timeouts_list=[]
    wait_time_list=[]
    wait_time_per_list=[]
    for name1,group1 in event_name_group:
        event_name=name1
        total_waits = group1['total_waits'].values[0] - group1['total_waits'].values[-1]         
        total_timeouts = group1['total_timeouts'].values[0] - group1['total_timeouts'].values[-1]
        if total_waits==0:
            total_waits_after=1
        else:
            total_waits_after=total_waits
        wait_time= round(int((group1['wait_time'].values[0] - group1['wait_time'].values[-1]))/100,2)                      
        wait_time_per= round(int((group1['wait_time'].values[0] - group1['wait_time'].values[-1]))/100/total_waits_after,2)
        event_name_list.append(event_name)
        total_waits_list.append(total_waits)
        total_timeouts_list.append(total_timeouts)
        wait_time_list.append(wait_time)
        wait_time_per_list.append(wait_time_per)
    columns=['event_name','wait_time','total_waits','wait_time_per','total_timeouts']
    topsql=pd.DataFrame({'event_name':event_name_list,'wait_time':wait_time_list,'total_waits':total_waits_list,'wait_time_per':wait_time_per_list,'total_timeouts':total_timeouts_list},columns=columns)
    top10=topsql.sort_values(by=['wait_time'], ascending=False).head(top).values
    idle_event=['rdbms ipc message']
    #top10=topsql[topsql.event_name not in idle_event].sort_values(by=['wait_time'], ascending=False).head(top).values
    result['top10sql']=top10
    return (result)







 

if __name__ == '__main__':
    endtime=1438567200+60
    starttime=1438563600
    ipaddress='10.65.1.110'
    tnsname='mesft'
    topsql_type='buffergets'
    result= check_topsql_final(starttime,endtime,ipaddress,tnsname,topsql_type)
    print (result)










