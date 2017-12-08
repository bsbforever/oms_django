import re
import os
import subprocess
import cx_Oracle
#from sendmail import *


def gettemputilization(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/gettempusage.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchone()
    return row[0]

def gettempusagetext(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/gettempusagetext.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchall()
    if row is not None:
        return row
    else:
        return False

def getundousage(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/getundousage.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchone()
    return row[0]

def getlibhit(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/getlibhit.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchone()
    return row

def getdichit(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/getdichit.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchone()
    return row

def getcachehit(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/getcachehit.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchone()
    return row

def getsqlplan(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/sql_plan_9i.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchall()
    return row

def gettopsegment(cursor):
    fp=open(os.environ['HOME_DIR']+'/mysite/monitor/command/sql/gettopsegment.sql','r') 
    fp1=fp.read()
    s=cursor.execute(fp1)
    fp.close()
    row=s.fetchall()
    return row

def getbuffergets(cursor):
    s=cursor.execute('select hash_value, abs(buffer_gets),abs(executions) ,abs(cpu_time),abs(elapsed_time),module,substr(sql_text,0,40) from v$sqlarea where abs(buffer_gets)>10000')
    row=s.fetchall()
    return row

def getdiskreads(cursor):
    s=cursor.execute('select hash_value, abs(disk_reads),abs(executions) ,abs(cpu_time),abs(elapsed_time),module,substr(sql_text,0,40) from v$sqlarea where abs(disk_reads)>10000')
    row=s.fetchall()
    return row

def getelapsedtime(cursor):
    s=cursor.execute('select hash_value, abs(elapsed_time),abs(executions) ,abs(cpu_time),module,substr(sql_text,0,40) from v$sqlarea where abs(elapsed_time)>1000000000')
    row=s.fetchall()
    return row

def getcputime(cursor):
    s=cursor.execute('select hash_value, abs(cpu_time),abs(executions) ,abs(elapsed_time),module,substr(sql_text,0,40) from v$sqlarea where abs(cpu_time)>1000000000')
    row=s.fetchall()
    return row

def gettopevent(cursor):
    s=cursor.execute('select event,abs(total_waits),abs(total_timeouts),abs(time_waited) from v$system_event')
    row=s.fetchall()
    return row

def getloadprofile1(cursor):
    s=cursor.execute('select name, abs(value) from v$sysstat where name in (\'parse count (hard)\',\'parse count (total)\',\'physical reads\',\'session logical reads\',\'user commits\',\'user rollbacks\') order by name')
    row=s.fetchall()
    return row

def getloadprofile(cursor):
    s=cursor.execute('select name, abs(value) from v$sysstat where name in (\'parse count (hard)\',\'parse count (total)\',\'physical reads\',\'session logical reads\',\'user commits\',\'user rollbacks\',\'user calls\',\'sorts (disk)\',\'logons cumulative\',\'redo size\',\'execute count\',\'table fetch by rowid\',\'table fetch continued row\',\'table scan rows gotten\',\'CPU used by this session\') order by name')
    row=s.fetchall()
    return row

def getdbtime(cursor):
    s=cursor.execute('select abs(value) from v$sys_time_model where stat_name=\'DB time\'')
    row=s.fetchall()
    return row[0][0]

def getsessionwait(cursor):
    s=cursor.execute('select substr(a.sql_text,0,50),a.HASH_VALUE,c.event,c.p1,c.P1RAW,c.p1text,c.p2,c.p2raw,c.p2text,c.p3,c.p3raw,c.p3text from v$sqlarea a, v$session b, v$session_wait c where a.hash_value = b.SQL_HASH_VALUE and b.sid = c.sid and c.event in (\'db file scattered read\',\'db file sequential read\',\'SQL*Net message from dblink\',\'sbtwrite2\',\'SQL*Net more data from dblink\',\'log file sync\')')
    row=s.fetchall()
    return row

def getsqlplan(cursor,sqlid):
    cursor.execute('select a.id,a.child_number,a.depth,a.operation,a.options,a.object_owner,a.object_name,a.object_node,a.cost,a.cardinality,a.bytes,a.io_cost,a.access_predicates,a.filter_predicates from v$sql_plan a where hash_value=\''+sqlid+'\'')
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
        row=gettopsegment(cursor)
        cursor.close()
        db.close()
        for i in row:
            print (i)














