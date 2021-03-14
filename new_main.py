# -*- coding: utf-8 -*-


"""
李运辰 2021-3-14

公众号：python爬虫数据分析挖掘
B站 ： python爬虫数据分析挖掘
"""


import requests
from lxml import etree
import random
import json

headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
            'cookie':'__secdyid=d95e39d0b5a512e1c35c5fdea59dcdd21b2758d39550e2c8021615635656; JSESSIONID=2DAE0DABD2DE9BB5D05335B2DE3AF8FF; PEAR_UUID=c32ee57d-4445-49f6-859a-a0a0fc054f1b; _uab_collina=161563565701204982722716; p_h5_u=C94D957E-E1CB-4130-9DF3-DDA387A42A8B; Hm_lvt_9707bc8d5f6bba210e7218b8496f076a=1615635658; UM_distinctid=1782b63b68f38-0331dcb7c2707d-5771133-100200-1782b63b690362; acw_tc=76b20f7116156407099735155e6bf791512b521ca0b97962f9cc398bc56d3a; CNZZDATA1260553744=1236015902-1615633517-%7C1615639181; Hm_lpvt_9707bc8d5f6bba210e7218b8496f076a=1615641462; SERVERID=ed8d5ad7d9b044d0dd5993c7c771ef48|1615641673|1615635656',
            'Host':'www.pearvideo.com',
        }



###下载视频
def down(name,url):
    headers_down = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
        'cookie': '__secdyid=d95e39d0b5a512e1c35c5fdea59dcdd21b2758d39550e2c8021615635656; JSESSIONID=2DAE0DABD2DE9BB5D05335B2DE3AF8FF; PEAR_UUID=c32ee57d-4445-49f6-859a-a0a0fc054f1b; _uab_collina=161563565701204982722716; p_h5_u=C94D957E-E1CB-4130-9DF3-DDA387A42A8B; Hm_lvt_9707bc8d5f6bba210e7218b8496f076a=1615635658; UM_distinctid=1782b63b68f38-0331dcb7c2707d-5771133-100200-1782b63b690362; acw_tc=76b20f7116156407099735155e6bf791512b521ca0b97962f9cc398bc56d3a; CNZZDATA1260553744=1236015902-1615633517-%7C1615639181; Hm_lpvt_9707bc8d5f6bba210e7218b8496f076a=1615641462; SERVERID=ed8d5ad7d9b044d0dd5993c7c771ef48|1615641673|1615635656',
        'Host': 'video.pearvideo.com',

    }
    r = requests.get(url,headers=headers_down)
    with open("lyc/"+str(name)+".mp4", 'wb+') as f:
        f.write(r.content)

#获取到真实的MP4地址
def getmp4(countid):

    #countid = "1721926"

    url = "https://www.pearvideo.com/videoStatus.jsp?contId=" + str(countid) + "&mrd=" + str(random.random())
    headers_id = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
        'cookie': '__secdyid=d95e39d0b5a512e1c35c5fdea59dcdd21b2758d39550e2c8021615635656; JSESSIONID=2DAE0DABD2DE9BB5D05335B2DE3AF8FF; PEAR_UUID=c32ee57d-4445-49f6-859a-a0a0fc054f1b; _uab_collina=161563565701204982722716; p_h5_u=C94D957E-E1CB-4130-9DF3-DDA387A42A8B; Hm_lvt_9707bc8d5f6bba210e7218b8496f076a=1615635658; UM_distinctid=1782b63b68f38-0331dcb7c2707d-5771133-100200-1782b63b690362; acw_tc=76b20f7116156407099735155e6bf791512b521ca0b97962f9cc398bc56d3a; CNZZDATA1260553744=1236015902-1615633517-%7C1615639181; Hm_lpvt_9707bc8d5f6bba210e7218b8496f076a=1615641462; SERVERID=ed8d5ad7d9b044d0dd5993c7c771ef48|1615641673|1615635656',
        'Host': 'www.pearvideo.com',
        'Referer': 'https://www.pearvideo.com/video_' + str(countid),

    }
    res = requests.get(url, headers=headers_id)
    res.encoding = 'utf-8'
    text = json.loads(res.text)



    videoInfo = text['videoInfo']['videos']['srcUrl']
    s1 = videoInfo.split("-")[0][0:-13]
    s2 = "cont-" + str(countid) + "-"
    murl = videoInfo.split("-")
    s3 = murl[1] + "-" + murl[2] + "-hd.mp4"
    return s1+s2+s3


###获取视频列表
def getlist():
    url = "https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=5&start=36"
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    text = res.text
    selector = etree.HTML(text)
    list = selector.xpath('//*[@class="categoryem"]')

    for i in list:
        href = i.xpath('.//div[@class="vervideo-bd"]/a/@href')[0]
        title = i.xpath('.//div[@class="vervideo-title"]/text()')[0]

        mp4ulr = getmp4(href.replace("video_",""))
        print("标题="+str(title))
        print("mp4播放地址="+str(mp4ulr))
        down(title,mp4ulr)

getlist()
#getmp4()

"""
源码获取方式：
公众号：python爬虫数据分析挖掘

回复：梨视频反爬

总结：
1.获取视频列表（反爬1：异步加载）
2.解析真实的mp4播放链接（根据id获取虚拟mp4地址，通过拼接方式获取真实mp4地址）
3.根据mp4地址去下载视频，实现批量下载

加群学习：公众号后台点击 加群学习  （群里有大佬，有老板，经常发红包）
"""