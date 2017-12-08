#!/usr/bin/python
#coding=utf-8
import MySQLdb
import os
import paramiko
from sendmail_mail import *
conn=MySQLdb.connect(host='localhost',user='oracle',passwd='dgvtG@ng1',db='oracle',port=3306)
cur=conn.cursor()
sql='SELECT ipaddress,username,password ,os,oracle_log FROM oracle.monitor_linuxlist where monitor_type=1 and oracle_log is not null  and oracle_log !=\'\' ;'
cur.execute(sql)
row=cur.fetchall()
cur.close()
conn.close()
mailcontent=[]
for i in row:
    ipaddress=i[0]
    username=i[1]
    password=i[2]
    os=i[3]
    path=i[4]
    try:
        if os=='linux':
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ipaddress,port=22,username=username,password=password)
            command='grep  -E \'ORA-|Checkpoint|Error\' '+path
            stdin,stdout,stderr=ssh.exec_command(command)
            err=stderr.readlines()
            if len(err) != 0:
                result='command error on ' +str(ipaddress)+' '+str(err)
                mailcontent.append(result)
            else:
                stdout_content=stdout.readlines()
		#print stdout_content
		#print ipaddress
            if len(stdout_content)!=0:
                result='\n'.join(stdout_content)
                result= 'Oralce log on '+ipaddress+ ' have errors\n '+path+'\n'+result
                mailcontent.append(result)
            else:
                pass
            ssh.close()
            #print mailcontent

        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ipaddress,port=22,username=username,password=password)
            command='grep  -E \'ORA-|Checkpoint|Error\' '+path
            stdin,stdout,stderr=ssh.exec_command(command)
            err=stderr.readlines()
            if len(err) != 0:
                result='command error on ' +str(ipaddress)+' '+str(err)
                mailcontent.append(result)
            else:
                stdout_content=stdout.readlines()
            if len(stdout_content)!=0:
                result='\n'.join(stdout_content)
                result= 'Oralce log on '+ipaddress+ ' have errors\n '+ path+'\n'+result
                #result=result.decode('utf8')
                mailcontent.append(result)
            else:
                pass
            ssh.close()
             #print mailcontent
    except Exception as e:
        mailcontent.append(str(e)+ ipaddress)



if len(mailcontent) !=0:
    title=' Oracle Log Check '
    mailcontent='\n'.join(mailcontent)
    send_mail_mail(to_list,title,mailcontent)
