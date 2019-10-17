import requests
from bs4 import BeautifulSoup
import webbrowser
import re
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
# def is_stat():

def parserLinks_Titles(html): #获取视频播放地址
    soup = BeautifulSoup(html,"html.parser")
    links = []
    titles = []
    for a in soup.find_all('a',_stat=re.compile('video:poster_')):#筛选出播放的地址
            if a.attrs['_stat'] == 'video:poster_tlelist':#筛选出播放的地址'video:poster_tlelist'"video:poster_num"
                link = a.attrs['href']
                title = a.attrs['title']
                links.append(link)
                titles.append(title)
            elif a.attrs['_stat'] == "video:poster_num":
                link = a.attrs['href']
                links.append(link)


    return links,titles

def composeurl(link,linenum='1'):#通过API获取视频播放后的解析地址
    Nhref=API[eval(linenum)-1]+link
    return Nhref

def broadcast(playUrl,linenum=None):
    if len(linenum) == 0:
        Nhref = composeurl(playUrl)  # 视频API破解
    else:
        Nhref = composeurl(playUrl,linenum)  # 视频API破解
        # print(Nhref)
    webbrowser.open(Nhref)  # 打开浏览器播放

def work():
    keyword = input("请输入要搜索的关键字：")
    html = getKeywordResult(keyword)
    (links,titles) = parserLinks_Titles(html)
    count = 1
    #lineum = 0  #播放线路默认0
    for title in titles:  #显示搜索到的内容标题
        print("[{:^3}]{}".format(count, title))
        count += 1
    # for link in links:
    #     print(link)
    i = input("请输入要播放的内容的序号（数字123...）：")
    print("输入0回到搜索关键字，支持重复更换线路")
    while (1):
        linenum = input("请输入要播放的线路123...共{}条(默认为1)：".format(len(API)))
        if linenum == '0':
            break
        else:
            broadcast(links[eval(i) - 1], linenum)  # 打开浏览器播放
    # print(Nhref)

def main():
    try:
        work()
    except:
        print("破解失败，请向管理员反应。")

while(1):
    main()