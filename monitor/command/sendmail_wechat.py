#!/usr/bin/python
#coding=utf8
import urllib
import requests
import json
import sys

def GetToken():
    Corpid='ww308306017cc53c84'              # 企业ID
    CorpSecret='5_vWbwROiUQJkc2wBEPxkPeGelovs2NsJ_qpvx2bW_M' #企业号应用的Secret值
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + Corpid + '&corpsecret=' + CorpSecret
    #print  (gettoken_url)
    try:
        token_file =requests.get(gettoken_url)
    except Exception as e:
        print (e)
    token_data = token_file.text
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token

def Send_Message(Token,Tag,Subject,Content):

    post_data={
       'touser' : '',            #通讯录用户ID
       'toparty' :'',            #通讯录组ID
       'totag' : Tag,            #通讯录标签ID
       'msgtype' : 'text',
       'agentid' : 1000002,      #企业号应用的agentid
       'text' : {
           'content' : Subject+'\n'+Content
           #'content' : SubjectContent
       },
       'safe':0
    }

    #print (post_data)
    post_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+Token
    #json_post_data = json.dumps(post_data,False,False)

    try:
        r =requests.post(post_url,data=json.dumps(post_data))
        #r =requests.post(post_url,data=json.dumps(post_data,ensure_ascii=False))
        #request_post = urllib.request.urlopen(post_url,json_post_data.encode(encoding='UTF8'))
    except Exception as e:
        print ('sss'+ str(e))
    #print (request_post.text)



if __name__ == '__main__':
    Corpid='ww308306017cc53c84'
    CorpSecret='5_vWbwROiUQJkc2wBEPxkPeGelovs2NsJ_qpvx2bW_M'
    #User = sys.argv[1]
    #Party=sys.argv[2]
    #Subject = sys.argv[3]
    #Content = sys.argv[4]
    Tag='2'
    Subject='服务器空间报警'
    Content='磁盘满啦'
    Token=GetToken()
    Send_Message(Token,Tag,Subject,Content)
