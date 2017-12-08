#coding=utf-8
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from monitor.models import oraclelist
from monitor.models import *
import os
import cx_Oracle
import time
from monitor.command.sendmail_phone import *
from monitor.command.getoracleinfo_topsql import *
class Command(BaseCommand):
    def handle(self, *args, **options):
        ip=oraclelist.objects.all().order_by('tnsname')
	#sql_time=str(time.time()).split('.')[0]
        segment_time=str(time.mktime(time.strptime(time.strftime('%Y%m%d %H', time.localtime()),'%Y%m%d %H'))).split('.')[0]
        for i in ip:
            if i.monitor_type==1 and i.performance_type==1:
                ipaddress1=i.ipaddress
                username=i.username
                password=i.password
                port=i.port
                tnsname1=i.tnsname
                try:
                    db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress1+':'+port+'/'+tnsname1 ,mode=cx_Oracle.SYSDBA)
                    cursor = db.cursor()
                    segmentchange=get_segment_change(cursor)
                    cursor.close()
                    db.close()
                    for o in segmentchange:
                        owner=o[0]
                        segment_name=o[1]
                        partition_name=o[2]
                        segment_type=o[3]
                        tablespace_name=o[4]
                        segment_bytes=o[5]
                        blocks=o[6]
                        insert=segmentsizechange(ipaddress=ipaddress1,tnsname=tnsname1,segment_time=segment_time,owner=owner,segment_name=segment_name,partition_name=partition_name,segment_type=segment_type,tablespace_name=tablespace_name,segment_bytes=segment_bytes,blocks=blocks)
                        insert.save()
	
                except Exception as e:
                    content= (i.ipaddress+' is Unreachable,The reason is '+str(e)).strip()
                    send_mail_phone(to_list,'Oracle Performance Monitor Exception Occured',content)
                    print( content)
