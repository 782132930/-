import requests
from bs4 import BeautifulSoup
import webbrowser
import re

#读取API
def getAPI():
    try:
        fo = open('API.txt','r') #打开API文件
        API=[]
        for line in fo:
            line = line.replace('\n','')
            API.append(line)
        fo.close()
        return API
    except:
        print("API文件打开失败，请检查原因")
API = getAPI()
# API = ['http://jx.kdy52.com/?url=', 'https://cdn.yangju.vip/k/?url=', 'https://jx.lache.me/cc/?url=','https://api.653520.top/vip/?url=',\
#        'https://jx.ab33.top/vip/?url=''https://vip.mpos.ren/v/?url=', 'https://jx.000180.top/jx/?url=','https://jx.km58.top/jx/?url=']
#腾讯视频搜索-静态页面
def getKeywordResult(keyword):
    url = 'https://v.qq.com/x/search/?q='+keyword
    url = url+'&stag=0&smartbox_ab='
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status() #如果状态不是200，引发异常
        r.encoding = 'utf - 8' #无论原来是什么编码，全部改用utf-8
        return r.text
    except:
        return ""
#搜索页面获取播放连续剧或电影的id
def parserid(html):
    soup = BeautifulSoup(html, "html.parser")
    ids=[]
    for div in soup.find_all('div', {'class': re.compile('result_item result_item_v')}):
        id=div.attrs['data-id']
        ids.append(id)
    return ids
#合成js链接
def getidResult(id):
    # url = 'https://s.video.qq.com/get_playsource?id=k4mutekomtrdbux&plat=2&type=4&data_\
    # type=2&video_type=3&plname=qq&range=1-15&otype=json&uid=d7098fe1-e7b1-404c-b1bb-7fca\
    # 5127980c&callback=_jsonp_1_3e8e&_t=1563440304958' #js链接
    url = 'https://s.video.qq.com/get_playsource?id='+id
    url=url+'&type=4&range=1-1000&otype=json' #拼凑js链接
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status() #如果状态不是200，引发异常
        r.encoding = 'utf - 8' #无论原来是什么编码，全部改用utf-8
        return r.text
    except:
        return ""
#解析js动态链接获取播放地址
def parserLinks_Titles(jsurl):
    i=0
    playUrls=[]
    titles=[]
    for s in jsurl: #统计无用的链接符号个数
        if s == '{':
            break
        i = i + 1
    str= jsurl[i:-1]   #保留后面有用的内容
    str = str.replace('false', 'False')
    dic = eval(str)
    for videoPlayList in dic['PlaylistItem'].get('videoPlayList'):
        playUrl=videoPlayList['playUrl']
        playUrls.append(playUrl)
        title=videoPlayList["title"]
        titles.append(title)
    return playUrls,titles
#通过API获取视频播放后的解析地址
def composeurl(link,linenum='1'):
    Nhref=API[eval(linenum)-1]+link
    return Nhref
#浏览器打开播放
def broadcast(playUrl,linenum=None):
    if len(linenum) == 0:
        Nhref = composeurl(playUrl)  # 视频API破解
    else:
        Nhref = composeurl(playUrl,linenum)  # 视频API破解
        # print(Nhref)
    webbrowser.open(Nhref)  # 打开浏览器播放

def work():
    restart=0
    keyword = input("请输入要搜索的关键字：")
    html = getKeywordResult(keyword)
    ids=parserid(html)
    jsurls=[]
    for id in ids:
        jsurl=getidResult(id) #合成js链接
        jsurls.append(jsurl)#获取js链接内容
        playUrlss=[]
        titless=[]
    for jsurl in jsurls:
        (playUrls,titles)=parserLinks_Titles(jsurl) #获取js链接的播放地址
        playUrlss=playUrlss+playUrls
        titless=titless+titles
    count = 1
    for title in titless:  #显示搜索到的内容标题
        print("[{:^3}]{}".format(count, title))
        count += 1
    i = input("请输入要播放的内容的序号（数字123...）：")
    print("输入0回到搜索关键字，支持重复更换线路")
    while (1):
        linenum = input("请输入要播放的线路123...共{}条(默认为1)：".format(len(API)))
        if linenum == '0':
            break
        else:
            broadcast(playUrlss[eval(i) - 1],linenum)#打开浏览器播放

def main():
    try:
        work()
    except:
        print("破解失败，请向管理员反应。")

while(1):
    main()







