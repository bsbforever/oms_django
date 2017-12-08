#coding=utf-8
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from oracle.models import *
import os
import cx_Oracle
import time
import threading
from monitor.command.getoracleinfo import *
    def handle(self, *args, **options):
        ip=oraclelist.objects.all().order_by('tnsname')
        sql_time=str(time.time()).split('.')[0]
        for i in ip:
            if i.monitor_type==1 and i.performance_type==1:
                    ipaddress1=i.ipaddress
                    username=i.username
                    password=i.password
                    port=i.port
                    tnsname1=i.tnsname
                        cursor = db.cursor()
                        buffergets=getbuffergets(cursor)
                        diskreads=getdiskreads(cursor)
                        elapsedtime=getelapsedtime(cursor)
                        cputime=getcputime(cursor)
                        cursor.close()
                        db.close()
                        for j in buffergets:
                            executions=j[2]
                            cpu_time=j[3]
                            elapsed_time=j[4]
                            module=j[5]
                            sql_text=j[6]
                            insert.save()

                            disk_reads=k[1]
                            executions=k[2]
                            cpu_time=k[3]
                            elapsed_time=k[4]
                            module=k[5]
                            sql_text=k[6]
                            insert.save()

                        for l in elapsedtime:
                            sql_id=l[0]
                            executions=l[2]
                            cpu_time=l[3]
                            elapsed_time=l[1]
                            module=l[4]
                            sql_text=l[5]
                            insert=oracle_elapsedtime(ipaddress=ipaddress1,tnsname=tnsname1,sql_time=sql_time,sql_id=sql_id,cpu_time=cpu_time,elapsed_time=elapsed_time,executions=executions,module=module,sql_text=sql_text)
                            insert.save()

                        for m in cputime:
                            sql_id=m[0]
                            executions=m[2]
                            cpu_time=m[1]
                            elapsed_time=m[3]
                            module=m[4]
                            sql_text=m[5]
                            insert=oracle_cputime(ipaddress=ipaddress1,tnsname=tnsname1,sql_time=sql_time,sql_id=sql_id,cpu_time=cpu_time,elapsed_time=elapsed_time,executions=executions,module=module,sql_text=sql_text)
                            insert.save()

                    except Exception , e:
                        content= (i.ipaddress+' is Unreachable,The reason is '+str(e)).strip()
                        send_mail(to_list,'Oracle Performance Monitor Exception Occured',content)
                        print content
