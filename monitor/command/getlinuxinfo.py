#!/usr/bin/python
#coding=utf-8
import os
import paramiko
def getunixspace(ssh):
	result=[]
	stdin,stdout,stderr=ssh.exec_command('bdf |awk \' NR>1 {if ($1==$NF){printf $1}else{print $0}}\'')
	err=stderr.readlines()
	if len(err) != 0:
	    print (err)
	    return False
	else:
	    stdout_content=stdout.readlines()
	result= stdout_content
	if  len(result) !=0:
	    return result
	else:
	    print ('can not find  unix bdf command')
def getlinuxspace(ssh):
	result=[]
	stdin,stdout,stderr=ssh.exec_command('df -h |awk \' NR>1 {if ($1==$NF){printf $1}else{print $0}}\'')
	err=stderr.readlines()
	if len(err) != 0:
	    print (err)
	    return False
	else:
	    stdout_content=stdout.readlines()
	result= stdout_content
	if  len(result) !=0:
	    return result
	else:
	    print ('can not find linux  df command')

def getlinuxcpu(ssh):
	result=[]
	stdin,stdout,stderr=ssh.exec_command('sar 2 3 |awk \'END {print 100-$NF}\'')
	err=stderr.readlines()
	if len(err) != 0:
	    print (err)
	    return False
	else:
	    stdout_content=stdout.readlines()
	result= stdout_content
	if  len(result) !=0:
	    return round(float(result[0].strip()),2)
	else:
	    print ('can not find linux sar  command')
def getlinuxmem(ssh):
	result=[]
	stdin,stdout,stderr=ssh.exec_command('free -m |awk \' NR==2 {print (($3 - $6 - $7)/$2)*100}\'')
	err=stderr.readlines()
	if len(err) != 0:
	    print (err)
	    return False
	else:
	    stdout_content=stdout.readlines()
	result= stdout_content
	if  len(result) !=0:
	    return round(float(result[0].strip()),2)
	else:
	    print ('can not find  linux free  command')
def getunixcpu(ssh):
	result=[]
	stdin,stdout,stderr=ssh.exec_command('sar 1 3 |awk \'END {print 100-$NF }\'')
	err=stderr.readlines()
	if len(err) != 0:
	    print (err)
	    return False
	else:
	    stdout_content=stdout.readlines()
	result= stdout_content
	if  len(result) !=0:
	    return round(float(result[0].strip()),2)
	else:
	    print ('can not find  unix sar  command')
def getunixmem(ssh):
	result=[]
	stdin,stdout,stderr=ssh.exec_command('swapinfo -tam | awk \'END { print $5}\'')
	err=stderr.readlines()
	if len(err) != 0:
	    print (err)
	    return False
	else:
	    stdout_content=stdout.readlines()
	result= stdout_content
	if  len(result) !=0:
	    return round(float(result[0].strip()[0:-1]),2)
	else:
	    print ('can not find unix  swapinf  command')

def getoraclelog(ssh,path):
        command='grep -l -E \'ORA-|Checkpoint|Error\' '+path
        stdin,stdout,stderr=ssh.exec_command(command)
        err=stderr.readlines()
        if len(err) != 0:
            print (err)
            return (err)
        else:
            stdout_content=stdout.readlines()
        if len(stdout_content)!=0: 
            result= stdout_content
            return (result)
        else:
            return 'noerror'
        print (result)





if __name__ == '__main__':
    hostname='10.65.1.85'
    username='asen'
    #password='nstx147)'
    password='asen'
    mailcontent=[]
    path='/oracle/NP1/saptrace/background/alert_NP1.log'
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,port=22,username=username,password=password)
        result=getlinuxcpu(ssh)
        ssh.close()
        if result:
            print (result)
        else:
            print ('There is something wrong with the command '+'on '+ hostname)
            #print (result)
    except Exception as e:  
        print (str(e))
	#print 's'
