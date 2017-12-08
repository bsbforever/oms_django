#coding=utf-8
from django.core.management.base import BaseCommand
from monitor.models import oraclelist
from monitor.models import oraclestatus
from monitor.command.getoracleinfo import *
class Command(BaseCommand):
    def handle(self, *args, **options):
        oraclestatus.objects.all().delete()
        ip=oraclelist.objects.all().order_by('tnsname')
        for i in ip:
            if i.monitor_type==1:
                    ipaddress1=i.ipaddress
                    username=i.username
                    password=i.password
                    port=i.port
                    tnsname1=i.tnsname
                    try:
                        db = cx_Oracle.connect(username+'/'+password+'@'+ipaddress1+':'+port+'/'+tnsname1 ,mode=cx_Oracle.SYSDBA)
                    except Exception , e:
                        content= (i.ipaddress+' is Unreachable,The reason is '+str(e)).strip()
                        print content
                    else:
			cursor = db.cursor()
                        dbsize=getdbsize(cursor)
                        tbstatus=getspace(cursor)
                        oracle_info=check_info(cursor)
                        sga_size=get_sga_size(cursor)
                        cursor.close()
                        db.close()
                        if oraclestatus.objects.filter(ipaddress=ipaddress1).filter(tnsname=tnsname1):
                            status=oraclestatus.objects.filter(ipaddress=ipaddress1)
                            status.update(**{'tnsname':tnsname1,'ipaddress':ipaddress1,'dbsize':dbsize,'tbstatus':tbstatus,'host_name':oracle_info[0],'version':oracle_info[1],'startup_time':oracle_info[2],'archiver':oracle_info[3],'sga_size':sga_size})
                        else:
                            createtnsname=oraclestatus(ipaddress=ipaddress1,tnsname=tnsname1)
                            createtnsname.save()
                            status=oraclestatus.objects.filter(ipaddress=ipaddress1).filter(tnsname=tnsname1)
                            status.update(**{'tnsname':tnsname1,'ipaddress':ipaddress1,'dbsize':dbsize,'tbstatus':tbstatus,'host_name':oracle_info[0],'version':oracle_info[1],'startup_time':oracle_info[2],'archiver':oracle_info[3],'sga_size':sga_size})
