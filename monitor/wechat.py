__author__ = 'bsbfo'
#coding=utf8
import requests
import json
corpid='ww308306017cc53c84'
corpsecret='5_vWbwROiUQJkc2wBEPxkPeGelovs2NsJ_qpvx2bW_M'

#token='j-JTA7JCP8d32RqaJupQR41dZRHdiczjTAU06WdFxACXrYlEnlSINWLD0b0ngAVxjn3sVUPt45S73N3O21C7V_9VfPf3mbgn73Al9wS5PX66szqWMy_Kon3HCSJ8W6eD4PtW7-Q3d9A8H-rjjmvKQ2kH4A0WcednZFBdeUGyI7iaPH9lUU78jVlLf0Z2x8gk'
def gettoken(corpid,corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    print  (gettoken_url)
    try:
        token_file =requests.get(gettoken_url)
    except Exception as e:
        print (e)
    token_data = token_file.text
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token

def sendmessage(token,post_data):
    print (post_data)
    post_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+str(token)
    try:
        r =requests.post(post_url,data=post_data)
    except Exception as e:
        print (e)
    print (r.text)


post_data={
   "touser" : "ShiYue",
   "toparty" : "",
   "totag" : "",
   "msgtype" : "text",
   "agentid" : 1000002,
   "text" : {
       "content" : "222"
   },
   "safe":0
}
token=gettoken(corpid,corpsecret)
print (token)
sendmessage(token,post_data)
