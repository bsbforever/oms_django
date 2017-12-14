import os
from sendmail_phone import *

def checkscriptstatus():
    mailcontent=[]
    fp=open("/home/oms/mysite/crontab.log",'r')
    content=fp.readlines()
    for i in content:
        mailcontent.append(i)
    if len(mailcontent)!=0:
        os.remove("/ezio/crontab.log")
        return mailcontent
    else:
        return False
if __name__ == '__main__':
    mailcontent=checkscriptstatus()
    if mailcontent is not False:
            content='\n'.join(mailcontent)
            send_mail_warning(to_list,'监控系统运行异常通知',content)

