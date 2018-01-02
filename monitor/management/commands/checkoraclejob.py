#coding=utf-8
from django.core.management.base import BaseCommand
from monitor.models import oraclelist
from monitor.command.getoracleinfo import *
from monitor.command.sendmail_phone import *
class Command(BaseCommand):
    def handle(self, *args, **options):
        mailcontent=[]
        ip=oraclelist.objects.all().order_by('tnsname')
        for i in ip:
            if i.monitor_type==1:
                ipaddress=i.ipaddress
                username=i.username
                password=i.password
                port=i.port
                tnsname=i.tnsname
                try:
                    db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress+':'+port+'/'+tnsname ,mode=cx_Oracle.SYSDBA)
                except Exception as  e:
                    content= (i.tnsname+' is Unreachable,The reason is '+str(e)).strip()
                    mailcontent.append(content)
                    #print (mailcontent)
                else:
                    cursor = db.cursor()
                    job=checkjob(cursor)
                    cursor.close()
                    db.close()
                    if job=='error':   
                        jobresult=  'The Job Have Errors On  '+i.tnsname
                        #print (jobresult)
                        mailcontent.append(jobresult)
        if len(mailcontent) != 0:
            mailcontent='\n'.join(mailcontent)
            send_mail_phone(to_list,'Oracle Job Status Monitor',mailcontent)
