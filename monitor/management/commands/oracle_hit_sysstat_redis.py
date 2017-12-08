#coding=utf-8
#coding=gbk
from django.core.management.base import BaseCommand
from monitor.models import oraclelist
from monitor.models import *
import os
import redis
import time
from monitor.command.getoracle_hit_sysstat import *
from monitor.command.sendmail_phone import *
class Command(BaseCommand):
    def handle(self, *args, **options):
        r=redis.StrictRedis()
        #nowtime=str(time.time()).split('.')[0]
        check_time=time.strftime('%Y%m%d %H', time.localtime())
        if check_time.split()[1]=='00':
            flag=1 #flag used to determin when should push two times
            nowtime=str(time.mktime(time.strptime(check_time,'%Y%m%d %H'))).split('.')[0]
            nnowtime=str(int(str(time.mktime(time.strptime(check_time,'%Y%m%d %H'))).split('.')[0])-1)
        else:
            flag=0
            nowtime=str(time.mktime(time.strptime(check_time,'%Y%m%d %H'))).split('.')[0]
        ip=oraclelist.objects.all().order_by('tnsname')
        for i in ip:
            if i.monitor_type==1 and i.hit_type==1:
                ipaddress1=i.ipaddress
                username=i.username
                password=i.password
                port=i.port
                tnsname1=i.tnsname
                try:
                    db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress1+':'+port+'/'+tnsname1 ,mode=cx_Oracle.SYSDBA)
                except Exception as  e:
                    content= (i.ipaddress+' is Unreachable,The reason is '+str(e)).strip()
                    send_mail_phone(to_list,'Oracle Performance Monitor Exception Occured',content)
                    print( content)
		#   break
                else:
                    cursor = db.cursor()
                    if i.version !='9i':
                        dbtime=getdbtime(cursor)
                        dbtimekey='DBTime='+ipaddress1+'='+tnsname1
                        dbtimevalue=nowtime+':'+str(dbtime)
                        r.lpush(dbtimekey,dbtimevalue)
                        if flag==1:
                            dbtimevalue1=nnowtime+':'+str(dbtime)
                            r.lpush(dbtimekey,dbtimevalue1)
			    
                    getlibhit1=getlibhit(cursor)
                    getdichit1=getdichit(cursor)
                    getcachehit1=getcachehit(cursor)
                    #undousage=getundousage(cursor)
                    tempusage=gettemputilization(cursor)
                    loadprofile=getloadprofile(cursor)
                    cursor.close()
                    db.close()
                    cpu_time=loadprofile[0][1]
                    execute=loadprofile[1][1]
                    logons=loadprofile[2][1]
                    hard_parse=loadprofile[3][1]
                    total_parse=loadprofile[4][1]
                    physical_reads=loadprofile[5][1]
                    redo_size=loadprofile[6][1]
                    logical_reads=loadprofile[7][1]
                    sorts=loadprofile[8][1]
                    fetch_by_rowid=loadprofile[9][1]
                    fetch_continued_row=loadprofile[10][1]
                    scan_rows_gotten=loadprofile[11][1]
                    user_calls=loadprofile[12][1]
                    user_commits=loadprofile[13][1]
                    user_rollbacks=loadprofile[14][1]
                    pinhit=getlibhit1[2]
                    reloadhit=getlibhit1[4]
                    dichit=getdichit1[2]
                    cachehit=getcachehit1[0]
                    
                    executekey='ExecuteCount='+ipaddress1+'='+tnsname1
                    executevalue=nowtime+':'+str(execute)
                    if flag==1:
                        executevalue1=nnowtime+':'+str(execute)
                        r.lpush(executekey,executevalue1)
                    r.lpush(executekey,executevalue)
                    
                    logonskey='Logons='+ipaddress1+'='+tnsname1
                    logonsvalue=nowtime+':'+str(logons)
                    if flag==1:
                        logonsvalue1=nnowtime+':'+str(logons)
                        r.lpush(logonskey,logonsvalue1)
                    r.lpush(logonskey,logonsvalue)
                    
                    redosizekey='RedoSize='+ipaddress1+'='+tnsname1
                    redosizevalue=nowtime+':'+str(redo_size)
                    if flag==1:
                        redosizevalue1=nnowtime+':'+str(redo_size)
                        r.lpush(redosizekey,redosizevalue1)
                    r.lpush(redosizekey,redosizevalue)
                    
                    sortskey='SortsDisk='+ipaddress1+'='+tnsname1
                    sortsvalue=nowtime+':'+str(sorts)
                    if flag==1:
                        sortsvalue1=nnowtime+':'+str(sorts)
                        r.lpush(sortskey,sortsvalue1)
                    r.lpush(sortskey,sortsvalue)
                    
                    cpukey='CPUTime='+ipaddress1+'='+tnsname1
                    cpuvalue=nowtime+':'+str(cpu_time)
                    if flag==1:
                        cpuvalue1=nnowtime+':'+str(cpu_time)
                        r.lpush(cpukey,cpuvalue1)
                    r.lpush(cpukey,cpuvalue)
                    
                    fetchbyrowidkey='FetchByRowid='+ipaddress1+'='+tnsname1
                    fetchbyrowidvalue=nowtime+':'+str(fetch_by_rowid)
                    if flag==1:
                        fetchbyrowidvalue1=nnowtime+':'+str(fetch_by_rowid)
                        r.lpush(fetchbyrowidkey,fetchbyrowidvalue1)
                    r.lpush(fetchbyrowidkey,fetchbyrowidvalue)
                    
                    fetchconrowkey='FetchContinuedRow='+ipaddress1+'='+tnsname1
                    fetchconrowvalue=nowtime+':'+str(fetch_continued_row)
                    if flag==1:
                        fetchconrowvalue1=nnowtime+':'+str(fetch_continued_row)
                        r.lpush(fetchconrowkey,fetchconrowvalue1)
                    r.lpush(fetchconrowkey,fetchconrowvalue)
                    
                    rowsgottenkey='ScanRowsGotten='+ipaddress1+'='+tnsname1
                    rowsgottenvalue=nowtime+':'+str(scan_rows_gotten)
                    if flag==1:
                        rowsgottenvalue1=nnowtime+':'+str(scan_rows_gotten)
                        r.lpush(rowsgottenkey,rowsgottenvalue1)
                    r.lpush(rowsgottenkey,rowsgottenvalue)
                    
                    usercallskey='UserCalls='+ipaddress1+'='+tnsname1
                    usercallsvalue=nowtime+':'+str(user_calls)
                    if flag==1:
                        usercallsvalue1=nnowtime+':'+str(user_calls)
                        r.lpush(usercallskey,usercallsvalue1)
                    r.lpush(usercallskey,usercallsvalue)
                    
                    hardparsekey='HardParse='+ipaddress1+'='+tnsname1
                    hardparsevalue=nowtime+':'+str(hard_parse)
                    if flag==1:
                        hardparsevalue1=nnowtime+':'+str(hard_parse)
                        r.lpush(hardparsekey,hardparsevalue1)
                    r.lpush(hardparsekey,hardparsevalue)
                    
                    totalparsekey='TotalParse='+ipaddress1+'='+tnsname1
                    totalparsevalue=nowtime+':'+str(total_parse)
                    if flag==1:
                        totalparsevalue1=nnowtime+':'+str(total_parse)
                        r.lpush(totalparsekey,totalparsevalue1)
                    r.lpush(totalparsekey,totalparsevalue)
                    
                    physicalreadskey='PhysicalReads='+ipaddress1+'='+tnsname1
                    physicalreadsvalue=nowtime+':'+str(physical_reads)
                    if flag==1:
                        physicalreadsvalue1=nnowtime+':'+str(physical_reads)
                        r.lpush(physicalreadskey,physicalreadsvalue1)
                    r.lpush(physicalreadskey,physicalreadsvalue)
                    
                    logicalreadskey='LogicalReads='+ipaddress1+'='+tnsname1
                    logicalreadsvalue=nowtime+':'+str(logical_reads)
                    if flag==1:
                        logicalreadsvalue1=nnowtime+':'+str(logical_reads)
                        r.lpush(logicalreadskey,logicalreadsvalue1)
                    r.lpush(logicalreadskey,logicalreadsvalue)
                    
                    commitskey='UserCommits='+ipaddress1+'='+tnsname1
                    commitsvalue=nowtime+':'+str(user_commits)
                    if flag==1:
                        commitsvalue1=nnowtime+':'+str(user_commits)
                        r.lpush(commitskey,commitsvalue1)
                    r.lpush(commitskey,commitsvalue)
                    
                    rollbackskey='UserRollbacks='+ipaddress1+'='+tnsname1
                    rollbacksvalue=nowtime+':'+str(user_rollbacks)
                    if flag==1:
                        rollbacksvalue1=nnowtime+':'+str(user_rollbacks)
                        r.lpush(rollbackskey,rollbacksvalue1)
                    r.lpush(rollbackskey,rollbacksvalue)
                    
                    reloadhitkey='ReloadHit='+ipaddress1+'='+tnsname1
                    reloadvalue=nowtime+':'+str(reloadhit)
                    if flag==1:
                        reloadvalue1=nnowtime+':'+str(reloadhit)
                        r.lpush(reloadhitkey,reloadvalue1)
                    r.lpush(reloadhitkey,reloadvalue)
                    
                    pinhitkey='PinHit='+ipaddress1+'='+tnsname1
                    pinvalue=nowtime+':'+str(pinhit)
                    if flag==1:
                        pinvalue1=nnowtime+':'+str(pinhit)
                        r.lpush(pinhitkey,pinvalue1)
                    r.lpush(pinhitkey,pinvalue)
                    
                    dichitkey='DicHit='+ipaddress1+'='+tnsname1
                    dicvalue=nowtime+':'+str(dichit)
                    if flag==1:
                        dicvalue1=nnowtime+':'+str(dichit)
                        r.lpush(dichitkey,dicvalue1)
                    r.lpush(dichitkey,dicvalue)
                    
                    cachehitkey='CacheHit='+ipaddress1+'='+tnsname1
                    cachevalue=nowtime+':'+str(cachehit)
                    if flag==1:
                        cachevalue1=nnowtime+':'+str(cachehit)
                        r.lpush(cachehitkey,cachevalue1)
                    r.lpush(cachehitkey,cachevalue)
                    
                    tempusagekey='TempUsage='+ipaddress1+'='+tnsname1
                    tempusagevalue=nowtime+':'+str(tempusage)
                    if flag==1:
                        tempusagevalue1=nnowtime+':'+str(tempusage)
                        r.lpush(tempusagekey,tempusagevalue1)
                    r.lpush(tempusagekey,tempusagevalue)
                    #undousagekey='UndoUsage='+ipaddress1+'='+tnsname1
                    #undousagevalue=nowtime+':'+str(undousage)
                    #r.lpush(undousagekey,undousagevalue)
