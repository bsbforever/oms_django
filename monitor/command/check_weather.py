__author__ = 'bsbfo'

#coding=utf8
import requests
import json
from sendmail_wechat import *
def now_weather(now):
    weather={}
    weather['date']=now['date']
    weather['now_day']=now['text_day']
    weather['now_night']=now['text_night']
    weather['now_high']=now['high']
    weather['now_low']=now['low']
    weather['now_direction']=now['wind_direction']
    weather['now_scale']=now['wind_scale']
    return weather

def next_weather(nextday):
    weather={}
    weather['date']=nextday['date']
    weather['next_day']=nextday['text_day']
    weather['next_night']=nextday['text_night']
    weather['next_high']=nextday['high']
    weather['next_low']=nextday['low']
    weather['next_direction']=nextday['wind_direction']
    weather['next_scale']=nextday['wind_scale']
    return weather

def stop_using_unicode(x):
    def unicode_to_str(y):
        return y.normalize("NFKD").encode("ascii", "ignore")
    return {unicode_to_str(k): unicode_to_str(v) for k, v in x.items()}
if __name__=='__main__':
    url='https://api.seniverse.com/v3/weather/daily.json?key=bfaubqmx0hbkdqbb&location=suzhou&language=zh-Hans&unit=c&start=0&days=5'

    r = requests.get(url)
    content=r.text
    content =json.loads(content)
    result=content['results'][0]
    #result=dict([(k.encode('ascii','ignore'), v.encode('ascii','ignore')) for k, v in result.items()])
    #result=stop_using_unicode(result)
    location=result['location']['name']

    now=result['daily'][0]

    #now_weather=now_weather(now)

    nextday=result['daily'][1]

    now_weather=now_weather(now)
    next_weather=next_weather(nextday)

    
    #print (next_weather)


    result_now=location+' '+now_weather['date']+' 天气预报: \n'+'白天: '+now_weather['now_day']+' 夜晚: '+now_weather['now_night']+'\n'+'最低气温: '+now_weather['now_low']+' 最高气温: '+now_weather['now_high']+'\n'+now_weather['now_direction']+'风 '+now_weather['now_scale']+'级'
    result_next=location+' '+next_weather['date']+' 天气预报: \n'+'白天: '+next_weather['next_day']+' 夜晚: '+next_weather['next_night']+'\n'+'最低气温: '+next_weather['next_low']+' 最高气温: '+next_weather['next_high']+'\n'+next_weather['next_direction']+'风 '+next_weather['next_scale']+'级'
    result=str(result_now+'\n\n\n\n'+result_next)
    token=GetToken()
    Send_Message(token,2,'今明天气预报',result  )


    #print (type(result_now))

