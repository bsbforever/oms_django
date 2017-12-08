from __future__ import unicode_literals

from django.db import models

# Create your models here.


class oraclelist(models.Model):
    ipaddress=models.GenericIPAddressField()
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    port=models.CharField(max_length=50)
    tnsname=models.CharField(max_length=100)
    version=models.CharField(max_length=100)
    charset=models.CharField(max_length=100)
    ncharset=models.CharField(max_length=100)
    hostname=models.CharField(max_length=100)
    alertpath=models.CharField(max_length=300)
    content=models.CharField(max_length=300)
    monitor_type=models.IntegerField(default=1)
    performance_type=models.IntegerField(default=0)
    hit_type=models.IntegerField(default=1)
    def __str__(self):
        return self.ipaddress
    class Meta:
        app_label='monitor'


class oraclestatus(models.Model):
    tnsname=models.CharField(max_length=100)
    ipaddress=models.GenericIPAddressField()
    dbsize=models.CharField(max_length=50)
    tbstatus=models.CharField(max_length=200)
    host_name=models.CharField(max_length=50,default='host')
    version=models.CharField(max_length=50,default='10')
    startup_time=models.CharField(max_length=50,default='2015')
    archiver=models.CharField(max_length=20,default='opened')
    sga_size=models.IntegerField(default=0)

    def __str__(self):
        return self.tnsname
    class Meta:
        app_label='monitor'


class oracle_buffergets(models.Model):
    ipaddress=models.GenericIPAddressField()
    tnsname=models.CharField(max_length=50)
    sql_time=models.BigIntegerField(blank=True)
    sql_id=models.CharField(max_length=50)
    buffer_gets=models.BigIntegerField(blank=True)
    executions=models.BigIntegerField(blank=True)
    cpu_time=models.BigIntegerField(blank=True,null=True)
    elapsed_time=models.BigIntegerField(blank=True,null=True)
    module=models.CharField(max_length=65,null=True)
    sql_text=models.CharField(max_length=1000)
    def __str__(self):
        return self.tnsname
    class Meta:
        app_label='monitor'

class oracle_diskreads(models.Model):
    ipaddress=models.GenericIPAddressField()
    tnsname=models.CharField(max_length=50)
    sql_time=models.BigIntegerField(blank=True)
    sql_id=models.CharField(max_length=50)
    disk_reads=models.BigIntegerField(blank=True)
    executions=models.BigIntegerField(blank=True)
    cpu_time=models.BigIntegerField(blank=True,null=True)
    elapsed_time=models.BigIntegerField(blank=True,null=True)
    module=models.CharField(max_length=65,null=True)
    sql_text=models.CharField(max_length=1000)
    def __str__(self):
        return self.tnsname
    class Meta:
        app_label='monitor'

class oracle_elapsedtime(models.Model):
    ipaddress=models.GenericIPAddressField()
    tnsname=models.CharField(max_length=50)
    sql_time=models.BigIntegerField(blank=True)
    sql_id=models.CharField(max_length=50)
    executions=models.BigIntegerField(blank=True)
    cpu_time=models.BigIntegerField(blank=True,null=True)
    elapsed_time=models.BigIntegerField(blank=True,null=True)
    module=models.CharField(max_length=65,null=True)
    sql_text=models.CharField(max_length=1000)
    def __str__(self):
        return self.tnsname
    class Meta:
        app_label='monitor'

class oracle_cputime(models.Model):
    ipaddress=models.GenericIPAddressField()
    tnsname=models.CharField(max_length=50)
    sql_time=models.BigIntegerField(blank=True)
    sql_id=models.CharField(max_length=50)
    executions=models.BigIntegerField(blank=True)
    elapsed_time=models.BigIntegerField(blank=True,null=True)
    cpu_time=models.BigIntegerField(blank=True,null=True)
    module=models.CharField(max_length=65,null=True)
    sql_text=models.CharField(max_length=1000)
    def __str__(self):
        return self.tnsname
    class Meta:
        app_label='monitor'


class oracle_topevent(models.Model):
    ipaddress=models.GenericIPAddressField()
    tnsname=models.CharField(max_length=50)
    sql_time=models.CharField(max_length=100)
    event_name=models.CharField(max_length=100)
    total_waits=models.BigIntegerField(blank=True)
    total_timeouts=models.BigIntegerField(blank=True)
    wait_time=models.BigIntegerField(blank=True)
    def __str__(self):
        return self.tnsname
    class Meta:
        app_label='monitor'


class segmentsizechange(models.Model):
    ipaddress=models.GenericIPAddressField()
    tnsname=models.CharField(max_length=20)
    segment_time=models.CharField(max_length=20)
    owner=models.CharField(max_length=20)
    segment_name=models.CharField(max_length=50)
    partition_name=models.CharField(max_length=50,null=True)
    segment_type=models.CharField(max_length=20)
    tablespace_name=models.CharField(max_length=50)
    segment_bytes=models.BigIntegerField()
    blocks=models.BigIntegerField()
    def __str__(self):
        return self.ipaddress
    class Meta:
        app_label='monitor'

class linuxlist(models.Model):
    ipaddress=models.GenericIPAddressField(primary_key=True)
    hostname=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    os=models.CharField(max_length=50)
    oracle_log=models.CharField(max_length=300,blank=True,null=True)
    os_log=models.CharField(max_length=300,blank=True,null=True)
    monitor_type=models.IntegerField(default=1)
    performance_type=models.IntegerField(default=0)
    def __str__(self):
        return self.ipaddress
    class Meta:
        app_label='monitor'

