#!/usr/bin/python
#coding=utf-8
from django import forms 
#from models import Blog    
#from models import alertevent
from monitor.models import oraclelist    
from monitor.models import linuxlist    
#from models import linuxlist    
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget 




class charts_cpumem_day(forms.Form):
    ip=[]
    ip1=linuxlist.objects.filter(performance_type=1).order_by('ipaddress')
    for i in ip1:
        ip.append((i.ipaddress+':'+i.hostname,i.ipaddress+'-'+i.hostname))
    type_choice=(
	('CPU','CPU'),
	('MEMORY','MEMORY'),
	)
    ip_initial=['10.60.14.60:NSAPDB1','10.65.1.102:mes-db1','10.65.1.109:LProDB-MESCP1','10.65.1.110:LProDB-MESFT1','10.65.1.117:DC1','10.65.1.37:ship2','10.65.202.201:lixora01','10.65.202.203:lixora02']
    performance_type=forms.ChoiceField(choices=type_choice)
    ipaddress=forms.MultipleChoiceField(
        required=True,
	widget=forms.CheckboxSelectMultiple,
	choices=ip,
	initial = [ip for ip in ip_initial]
	)
    #granularity = forms.IntegerField(initial=1)
    class Meta:
        app_label='monitor'

class charts_oracle_performance(forms.Form):
    ip=[]
    ip1=oraclelist.objects.filter(monitor_type=1).order_by('tnsname')
    for i in ip1:
        ip.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    type_choice=(
	('PhysicalReads','Physical Reads'),
	('LogicalReads','Logical Reads'),
	('DBTime','DB Time'),
	('CPUTime','CPU Time'),
	('HardParse','Hard Parse'),
	('TotalParse','Total Parse'),
	('UserCommits','User Commits'),
	('UserRollbacks','User Rollbacks'),
	('Logons','Logons'),
	('SortsDisk','Sorts Disk'),
	('UserCalls','User Calls'),
	('RedoSize','Redo Size'),
	('ExecuteCount','Execute Count'),
	('FetchByRowid','Fetch By Rowid'),
	('FetchContinuedRow','Fetch Continued Row'),
	('ScanRowsGotten','Scan Rows Gotten'),
	)
    ip_initial=[]
    ip_initial1=oraclelist.objects.filter(performance_type=1).order_by('tnsname')
    for i in ip_initial1:
        ip_initial.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    performance_type=forms.ChoiceField(choices=type_choice)
    ipaddress=forms.MultipleChoiceField(
        required=True,
	widget=forms.CheckboxSelectMultiple,
	choices=ip,
	initial = [ip_[0] for ip_ in ip_initial]
	)
    #granularity = forms.IntegerField(initial=1)
    class Meta:
        app_label='monitor'

class charts_performance(forms.Form):
    ip=[]
    ip1=oraclelist.objects.filter(monitor_type=1).order_by('tnsname')
    for i in ip1:
        ip.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    ipaddress=forms.ChoiceField(choices=ip)
    type_choice=(
        ('PhysicalReads','Physical Reads'),
        ('LogicalReads','Logical Reads'),
        ('DBTime','DB Time'),
        ('CPUTime','CPU Time'),
        ('HardParse','Hard Parse'),
        ('TotalParse','Total Parse'),
        ('UserCommits','User Commits'),
        ('UserRollbacks','User Rollbacks'),
        ('Logons','Logons'),
        ('SortsDisk','Sorts Disk'),
        ('UserCalls','User Calls'),
        ('RedoSize','Redo Size'),
        ('ExecuteCount','Execute Count'),
        ('FetchByRowid','Fetch By Rowid'),
        ('FetchContinuedRow','Fetch Continued Row'),
        ('ScanRowsGotten','Scan Rows Gotten'),
        )
    performance_type=forms.ChoiceField(choices=type_choice)
    #granularity = forms.IntegerField(initial=1)
    class Meta:
        app_label='monitor'


class charts_oracle_topevent(forms.Form):
    ip=[]
    ip1=oraclelist.objects.filter(monitor_type=1).order_by('tnsname')
    for i in ip1:
        ip.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    #ipaddress=forms.ChoiceField(choices=ip)
    type_choice=(
        ('db file scattered read','db file scattered read'),
        ('db file sequential read','db file sequential read'),
        ('buffer busy waits','buffer busy waits'),
        ('log file sync','log file sync'),
        ('log file single write','log file single write'),
        ('direct path read','direct path read'),
        ('Backup: sbtbackup','Backup: sbtbackup'),
        ('SQL*Net message from dblink','SQL*Net message from dblink'),
        ('SQL*Net more data from dblink','SQL*Net more data from dblink'),
        ('SQL*Net more data from client','SQL*Net more data from client'),
        )
    ip_initial=[]
    ip_initial1=oraclelist.objects.filter(performance_type=1).order_by('tnsname')
    for i in ip_initial1:
        ip_initial.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    performance_type=forms.ChoiceField(choices=type_choice)
    ipaddress=forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=ip,
        initial = [ip_[0] for ip_ in ip_initial]
        )
    #granularity = forms.IntegerField(initial=1)
    class Meta:
        app_label='monitor'



class charts_topsql(forms.Form):
    ip=[]
    ip1=oraclelist.objects.filter(performance_type=1).order_by('ipaddress')
    for i in ip1:
        ip.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    ipaddress=forms.ChoiceField(choices=ip)
    type_choice=(
        ('diskreads:disk_reads','DiskReads'),
        ('buffergets:buffer_gets','BufferGets'),
        ('elapsedtime:elapsed_time','ElapsedTime'),
        ('cputime:cpu_time','CpuTime'),
        ('topevent:wait_time','TopEvent'),
        ('segmentsizechange:segmentsizechange','TopSegmentChange'),
        ('physical reads:topsegment','SegmentPhysicalReads'),
        ('physical writes:topsegment','SegmentPhysicalWrites'),
        ('logical reads:topsegment','SegmentLogicalReads'),
        ('buffer busy waits:topsegment','SegmentBufferBusyWaits'),
        )
    topsql_type=forms.ChoiceField(choices=type_choice)
    top = forms.IntegerField(initial=10)
    class Meta:
        app_label='monitor'



class charts_addbaseline(forms.Form):
    ip=[]
    ip1=oraclelist.objects.filter(monitor_type=1).order_by('tnsname')
    for i in ip1:
        ip.append((i.ipaddress+':'+i.tnsname,i.ipaddress+'-'+i.tnsname))
    ipaddress=forms.ChoiceField(choices=ip)
    #granularity = forms.IntegerField(initial=1)
    class Meta:
        app_label='monitor'



class charts_hitratio(forms.Form):
    type_choice=(
        ('PinHit','PinHit'),
        ('ReloadHit','ReloadHit'),
        ('DicHit','DicHit'),
        ('CacheHit','CacheHit'),
        ('TempUsage','TempUsage'),
        )
    #ipaddress=forms.IPAddressField()
    granularity = forms.IntegerField(initial=1)
    ratio_type=forms.ChoiceField(choices=type_choice)
    class Meta:
        app_label='monitor'

