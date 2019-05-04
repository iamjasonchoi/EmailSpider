from urllib import parse
import urllib.request
import re
import time
import string

#获取页面信息
def getResponse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    request.add_header('Connection', 'keep-alive')
    try:
        response = urllib.request.urlopen(request,timeout = 15)
    except:
        print('time out')
    data = None
    try:
        data = response.read().decode('utf-8', "ignore")
    except UnicodeDecodeError:
        data = response.read()
    except:
        data=""
        time.sleep(15)
    return data

#获取小组链接列表
def getGroups(name):
    url = 'https://www.douban.com/group/search?cat=1019&q=' + urllib.parse.quote(name)
    date = getResponse(url)

    regexStr = r'https://www.douban.com/group/[A-Z0-9]*?/'
    group_regex = re.compile(regexStr, re.IGNORECASE)
    groups = re.findall(group_regex,date)
    #去除重复和精选
    groups = list(set(groups))
    jingxuanUrl = 'https://www.douban.com/group/search?cat=1019&q=explore'
    if jingxuanUrl in groups:
        groups.remove(jingxuanUrl)
    return groups

#获取话题列表
def GetTopics(url):
    data = getResponse(url)
    regexStr = r"https://www.douban.com/group/topic/[A-Z0-9]*?/"
    topic_regex = re.compile(regexStr,re.IGNORECASE)
    topics = re.findall(topic_regex,data)
    topics = list(set(topics))
    return topics

#从话题中获取邮箱
def get_emails(url):
    count = 0
    site = 1 
    list_emails = []
    mail_regex = re.compile(r'([A-Z0-9_+]+@[A-Z0-9]+\.[A-Z]{2,6})', re.IGNORECASE)
    while True:
        data = ""
        if site == 1:
            print(url)
            data = getResponse(url)
            count_regex_str = r'data-total-page=\"([\d]*?)\"'
            count_regex = re.compile(count_regex_str,re.IGNORECASE)
            count_list = re.findall(count_regex,data)     
            if len(count_list) == 0:
                count = 1
            else:
                count = eval(count_list[0])
            print(count)
        else:
            print(url + '?start=' + str((site-1)*100))
            data = getResponse(url + '?start=' + str((site-1)*100))

        #获取邮箱
        mails = re.findall(mail_regex,data)
        if 'business@douban.com' in mails:
            mails.remove('business@douban.com')
        if len(mails) > 0:
            print(mails)
        list_emails = list_emails + mails

        site = site + 1
        if site>count:
            break
        print('*'*20)
    return list(set(list_emails))
    

