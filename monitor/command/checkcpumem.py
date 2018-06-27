import os
from sendmail_phone import *
from sendmail_wechat import *
import redis
def warning_cpu():
    r=redis.StrictRedis()
    for i in r.keys():
        count=0
        result=i.decode().split('=')
        if result[0]=='CPU':
            mailcontent_warning=[]
            for j in range(0,5):
                cpu_utilization=r.lindex(i,j).decode().split(':')[1]
                if float(cpu_utilization)>80:
                    count=count+1
                if count==5:
                    mailcontent='Be Careful,The CPU Utilization Of '+ result[1] +' Is ' +str(cpu_utilization)+'% Used'
                    token=GetToken()
                    Send_Message(token,2,'Linux CPU Utilization Monitor',mailcontent)
  #  return mailcontent_warning


def warning_mem():
    r=redis.StrictRedis()
    for i in r.keys():
        count=0
        result=i.decode().split('=')
        if result[0]=='MEMORY':
            #print (i)
            mailcontent_warning=[]
            for j in range(0,5):
                mem_utilization=r.lindex(i,j).decode().split(':')[1]
                if float(mem_utilization)>96:
                    count=count+1
                if count==5:
                    mailcontent='Be Careful,The MEMORY Utilization Of '+ result[1] +' Is ' +str(mem_utilization)+'% Used'
                    token=GetToken()
                    Send_Message(token,2,'Linux MEMORY Utilization Monitor',mailcontent)
  #  return mailcontent_warning

if __name__ == '__main__':
    warning_cpu()
    warning_mem()

