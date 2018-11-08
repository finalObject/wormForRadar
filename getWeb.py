#!/usr/bin/python
import urllib.request as myUrl
import re
import datetime
# 每天中午12点执行，获取昨天00和12时的数据

nowTime = datetime.datetime.now()
yesterday = nowTime+datetime.timedelta(hours=-24)


path = '/home/wwwroot/default/zju/'
link=['00','00']
name=['00','00']
link[0] = yesterday.strftime('YEAR=%Y&MONTH=%m&FROM=%d00&TO=%d00&STNM=58457')
link[1] = yesterday.strftime('YEAR=%Y&MONTH=%m&FROM=%d12&TO=%d12&STNM=58457')
name[0] = yesterday.strftime('%Y-%m-%d-00')
name[1] = yesterday.strftime('%Y-%m-%d-12')
for i in range(2):
        req = myUrl.urlopen('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&'+link[i])

        buf=req.read()
        buf= buf.decode('utf-8')

        loc = re.search(r'<H2>.*?</H2>',buf).span()

        title = buf[loc[0]+4:loc[1]-5]

        loc1 = re.search(r'<H2>.*?</H2>',buf).span()[1]
        loc2 = re.search(r'<H3>.*?</H3>',buf).span()[0]
        buf = buf[loc1+7:loc2-7]
        f=open(path+"wyoming-data.txt","a");
        f.write(title)
        f.write('\n')
        f.write(buf)
        f.write('\n\n')
        f.close