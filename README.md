实验室同学需要，帮他写的一个扒取网页数据的小脚本。网页比较简单，是一个很普通的静态页面。<!--more-->

github：<a href="https://github.com/finalObject/wormForRadar">https://github.com/finalObject/wormForRadar</a>
原文链接：<a href="http://finalobject.cn/lucario/wormforradar">finalObject.cn</a>

在网页上进行请求之后可以发现，其实需要的网页就是一个按照请求数据的日期组织的一个链接，所以基本思路就是根据当天日期生成昨天两个时间点的链接，请求之后解析需要的字段，追加到<a href="http://finalobject.cn/zju/wyoming-data.txt">http://finalobject.cn/zju/wyoming-data.txt</a>文件里就行。
<pre class="lang:python decode:true " title="Python3 Code">#!/usr/bin/python
import urllib.request as myUrl
import re
import datetime
# 每天中午12点执行，获取昨天00和12时的数据

nowTime = datetime.datetime.now()
yesterday = nowTime+datetime.timedelta(hours=-24)


path = '/home/wwwroot/default/zju/'
link=['00','00']
name=['00','00']
link[0] = yesterday.strftime('YEAR=%Y&amp;MONTH=%m&amp;FROM=%d00&amp;TO=%d00&amp;STNM=58457')
link[1] = yesterday.strftime('YEAR=%Y&amp;MONTH=%m&amp;FROM=%d12&amp;TO=%d12&amp;STNM=58457')
name[0] = yesterday.strftime('%Y-%m-%d-00')
name[1] = yesterday.strftime('%Y-%m-%d-12')
for i in range(2):
        req = myUrl.urlopen('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&amp;TYPE=TEXT%3ALIST&amp;'+link[i])

        buf=req.read()
        buf= buf.decode('utf-8')

        loc = re.search(r'&lt;H2&gt;.*?&lt;/H2&gt;',buf).span()

        title = buf[loc[0]+4:loc[1]-5]

        loc1 = re.search(r'&lt;H2&gt;.*?&lt;/H2&gt;',buf).span()[1]
        loc2 = re.search(r'&lt;H3&gt;.*?&lt;/H3&gt;',buf).span()[0]
        buf = buf[loc1+7:loc2-7]
        f=open(path+"wyoming-data.txt","a");
        f.write(title)
        f.write('\n')
        f.write(buf)
        f.write('\n\n')
        f.close</pre>
直接给这个脚本添加执行权限，然后放到服务器的/root/bin/目录下

执行
<pre class="lang:sh decode:true ">crontab -e</pre>
crontab是一个linux下管理定时任务的软件，-e代表编辑配置文件，输入如下内容
<pre class="lang:sh decode:true ">SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
15 12 * * * getWeb.py</pre>
如果只输入第三行，貌似很容易出现问题，所以最好还是配置一下shell和path。一开始写的是12点执行一次，但是今天第一天运行的时候，发现返回了一个503错误，百度之后发现说是对方服务器的问题，担心可能是整点时间下对面服务器也在更新数据什么的，所以的脚本执行时间往后延迟了15分钟。

默认情况下可以使用
<pre class="lang:sh decode:true ">cat /var/spool/mail/root</pre>
来查看定时程序的输出信息，可以用来排错。

后续如果没有问题就不来更新了，如果明天还是不能正常执行，会进行后续的更新。可以考虑对原来python脚本里面的服务器请求进行异常处理，不停请求直到正常为止。