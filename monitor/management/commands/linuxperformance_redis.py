#coding=utf-8
#coding=gbk
from django.core.management.base import BaseCommand
from monitor.models import linuxlist
import os
import redis
import time
from time import ctime,sleep
import threading
from monitor.command.getlinuxinfo import *
class Command(BaseCommand):
    def handle(self, *args, **options):
        def getperformance(i):
            if i.monitor_type==1 and i.performance_type==1:
                    ipaddress=i.ipaddress
                    username=i.username
                    password=i.password
                    hostname1=i.hostname
                    try:
                        if i.os=='linux':
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=ipaddress,port=22,username=username,password=password)
                            linuxcpu=getlinuxcpu(ssh)
                            linuxmem=getlinuxmem(ssh)
                            ssh.close()
                            dskey='CPU='+ipaddress+'='+hostname1
                            value=nowtime+':'+ str(linuxcpu)
                            if flag==1:
                                value1=nnowtime+':'+ str(linuxcpu)
                                r.lpush(dskey,value1)
                            r.lpush(dskey,value)
			    
                            
                            dskey='MEMORY='+ipaddress+'='+hostname1
                            value=nowtime+':'+ str(linuxmem)
                            if flag==1:
                                value1=nnowtime+':'+ str(linuxmem)
                                r.lpush(dskey,value1)
                            r.lpush(dskey,value)
#			    print ipaddress+hostname1
                        else:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=ipaddress,port=22,username=username,password=password)
                            unixcpu=getunixcpu(ssh)
                            unixmem=getunixmem(ssh)
                            ssh.close()
                            dskey='CPU='+ipaddress+'='+hostname1
                            value=nowtime+':'+ str(unixcpu)
                            if flag==1:
                                value1=nnowtime+':'+ str(unixcpu)
                                r.lpush(dskey,value1)
                            r.lpush(dskey,value)
			    

                            dskey='MEMORY='+ipaddress+'='+hostname1
                            value=nowtime+':'+ str(unixmem)
                            if flag==1:
                                value1=nnowtime+':'+ str(unixmem)
                                r.lpush(dskey,value1)
                            r.lpush(dskey,value)
                    except Exception as e:
                        result1=str(e)+ipaddress
                        mailcontent.append(result1)
                        print (mailcontent)
                    time.sleep(10)
	#print 'get linux performance'
        mailcontent=[]
        r=redis.StrictRedis()
        check_time=time.strftime('%Y%m%d%H %M', time.localtime())
        if check_time.split()[1]=='00':
            flag=1 #flag used to determin when should push two times
            nowtime=str(time.mktime(time.strptime(check_time,'%Y%m%d%H %M'))).split('.')[0]
            nnowtime=str(int(str(time.mktime(time.strptime(check_time,'%Y%m%d%H %M'))).split('.')[0])-1)
        else:
            flag=0
            nowtime=str(time.mktime(time.strptime(check_time,'%Y%m%d%H %M'))).split('.')[0]
        ip=linuxlist.objects.all().order_by('ipaddress')
        threads=[]
        for i in ip:
            t1 = threading.Thread(target=getperformance,args=(i,))
            threads.append(t1)
        for t in threads:
           # t.setDaemon(True)
            t.start()
        t.join()
	#r.save()
        #print (mailcontent)
