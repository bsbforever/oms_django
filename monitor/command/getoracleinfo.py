import re
import os
import subprocess
import cx_Oracle
def getdbname(cursor):
    '''db = cx_Oracle.connect(username+'/'+password+'@'+ ipaddress+':'+'/'+tnsname)
    cursor = db.cursor()'''
    cursor.execute('select name from v$database')
    row=cursor.fetchone()
    dbname=row[0]
    return dbname

def getinstancename(cursor):
    cursor.execute('select instance_name from v$instance')
    row=cursor.fetchone()
    instancename=row[0]
    return instancename

def checkinvalidobject(cursor):
    cursor.execute('SELECT count(*) FROM dba_objects  WHERE status = \'INVALID\'')
    row=cursor.fetchone()
    return row[0]

def check_mv_compile_states(cursor):
    cursor.execute('SELECT count(*) FROM DBA_MVIEWS  WHERE COMPILE_STATE <> \'VALID\'')
    row=cursor.fetchone()
    return row[0]

def check_active_session_count(cursor):
    cursor.execute('SELECT count(*) from v$session where status=\'ACTIVE\'')
    row=cursor.fetchone()
    return row[0]


def checkjob(cursor):
    cursor.execute('select failures from dba_jobs a where round((sysdate-this_date)*24,2) >2 or failures<>0')
    #cursor.execute('select failures from dba_jobs')
    row=cursor.fetchone()
    if row is None:
        return 'normal'
    else:
        return 'error'

def checkactivesession(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/getsession.sql','r')
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchone()
    if row is None:
        return 'normal'
    else:
        return 'error'

def checkifrac(cursor):
    cursor.execute('select value from v$option where  parameter=\'Real Application Clusters\'')
    row=cursor.fetchone()
    result=row[0]
    return result

def checkdggap1(cursor):
    cursor.execute('SELECT * FROM V$ARCHIVE_GAP')
    row=cursor.fetchone()
    if row is None:
        j='normal'
        return j
    else:
        j='\n'.join(str(row))
	#j='error'
        return j

def checkdggap(cursor):
    cursor.execute('select t.completion_time,round((sysdate-t.completion_time)*24) gap  from v$archived_log t where t.applied = \'NO\' order by completion_time')
    row=cursor.fetchone()
    if row is None or int(row[1])<=6:
        return 'normal'
    else:
        return str(row[0])

def checksystemaccount(cursor):
    cursor.execute('SELECT  * FROM dba_users where username=\'SYSTEM\' and account_status<>\'OPEN\'')
    row=cursor.fetchone()
    if row is None:
        return 'normal'
    else:
        return 'error'

def checkexpiry(cursor):
    expiry=[]
    cursor.execute('select username,expiry_date ,round((EXPIRY_DATE-sysdate) ) DIF from dba_users where account_status =\'OPEN\' AND USERNAME<>\'SYS\'')
    row=cursor.fetchall()
    for i in row:
        if i[1] is not None and i[2]<0:
            expiry.append('The account '+str(i[0])+' will expired '+str(i[2])+' days')
        else:
            pass
    if len(expiry)!=0:
        return expiry
    else:
        return 'normal'
def checkram(cursor):
        cursor.execute('select status from v$rman_backup_job_details')
        row=cursor.fetchall()
        j=1
        try:
            for i in row:
                if j==30:
                    ram=i[0]
                    break
                else:
                    j=j+1
            return ram
        except:
            return 'None'            

def getdbsize(cursor):
    #cursor.execute('select trunc(sum(bytes)/1024/1024/1024) Total from dba_segments')
    cursor.execute('select trunc(sum(bytes)/1024/1024/1024) Total from dba_data_files')
    row=cursor.fetchone()
    result=row[0]
    return result    

def getsegsize(cursor):
    cursor.execute('select trunc(sum(bytes)/1024/1024/1024) Total from dba_segments')
    #cursor.execute('select trunc(sum(bytes)/1024/1024/1024) Total from dba_data_files')
    row=cursor.fetchone()
    result=row[0]
    return result    

def getspace(cursor):
    fp=open('/ezio/website/oracle/monitor/tablespacesize.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    result=[]
    row=s.fetchall()
    for i in row:
        if i[4]>98:
            result.append(i[0])
    result='|'.join(result)
    if len(result)==0:
        return 'normal'	
    else:
        return result

def getindex(cursor):
    fp=open('/ezio/website/oracle/monitor/getindex.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    result=[]
    row=s.fetchall()
    for i in row:
        result.append(i[0]+'.'+i[1])
    return result
    #return row
def checklock(cursor):
    fp1=open('/ezio/website/oracle/monitor/checklock.sql','r')
    fp=fp1.read()
    s=cursor.execute(fp)
    fp1.close()
    row1=s.fetchone()
    if row1 is None:
        j='normal'
        return  j
    else:
        fp2=open('/ezio/website/oracle/monitor/checklock.sql','r')
        fp=fp2.read()
        s=cursor.execute(fp)
        fp2.close()
        row=s.fetchall()
        for i in row:
            lockdate=str(i[7])
            get_dateinterval=cursor.execute('select floor((sysdate - to_date(\''+lockdate+'\',\'yyyy-mm-dd hh24:mi:ss\'))*24*60) from dual')
            date_interval=get_dateinterval.fetchone()
            if  date_interval[0]>30 :
		#print date_interval[0]
                return date_interval[0]
            else:
                return 'normal'


def checkalert(cursor):
    alert_log=[]
    try:
        #cursor.execute('select * from alert_ext where log like \'%ORA-%\'' )
        cursor.execute('select * from alert_ext where log like \'%ORA-%\' or log like \'%Checkpoint%\'' )
        row1=cursor.fetchone()
        if row1 is None:
            j='normal'
            return j
        else:
           # cursor.execute('select * from alert_ext where log like \'%ORA-%\'')
            cursor.execute('select * from alert_ext where log like \'%ORA-%\' or log like \'%Checkpoint%\'')
            row=cursor.fetchall()
            for i in row:
                alert_log.append(i[0])
            return alert_log
    except Exception as e:
        return 'nolog'

def check_info(cursor):
        cursor.execute('select host_name,version,to_char(startup_time,\'yyyy-mm-dd hh24:mi\')  ,status,archiver from  v$instance')
        row=cursor.fetchone()
        result=row
        return result
def get_sga_size(cursor):
        cursor.execute('select trunc(value/1024/1024)  from v$parameter where name =\'sga_max_size\'')
        row=cursor.fetchone()
        result=row[0]
        return result
	

def get_segment_change(cursor):
        cursor.execute('select owner,segment_name,partition_name,segment_type,tablespace_name,bytes,blocks from dba_Segments where bytes > 1024000000')
        row=cursor.fetchall()
        return row

if __name__ == '__main__':
    ipaddress='10.65.1.120'
    username='sys'
    password='ase_sys_n'
    port='1521'
    tnsname='dctest'
    try:
        db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
    except Exception as  e:
        content= (tnsname+' is Unreachable,The reason is '+ str(e)).strip()
        print (content)
        #mailcontent.append(content)
    else:
        cursor = db.cursor()
        #j=check_mv_compile_states(cursor)
        s=getactivesession(cursor)
        cursor.close()
        db.close()
        print (s)
