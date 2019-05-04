from urllib import parse
import urllib.request
import re
import time

#获取numbers
def gettiebalistnumbers(name):
    url = 'http://tieba.baidu.com/f?'
    word = {
            'kw': name,
            'pn': 0
            }
    word = parse.urlencode(word)
    url = url + word
    data = getresponse(url)

    guanzhu_restr = '<span class="card_menNum">([\s\S]*?)</span>'
    guanzhu_regex = re.compile(guanzhu_restr, re.IGNORECASE)
    guanzhu_list = re.findall(guanzhu_regex, data)
    guanzhu_number = eval(guanzhu_list[0].replace(',', ''))

    tiezi_restr = '<span class="card_infoNum">([\s\S]*?)</span>'
    tiezi_regex = re.compile(tiezi_restr, re.IGNORECASE)
    tiezi_list = re.findall(tiezi_regex, data)
    tiezi_number = eval(tiezi_list[0].replace(',', ''))

    zhuti_rester = '共有主题数<span class="red_text">([\s\S]*?)</span>个'
    zhuti_regex = re.compile(zhuti_rester, re.IGNORECASE)
    zhuti_list = re.findall(zhuti_regex, data)
    zhuti_number = eval(zhuti_list[0].replace(',', ''))

    return guanzhu_number, tiezi_number, zhuti_number

#获取帖子url列表
def gettiebalist(name):
    number_tuple = gettiebalistnumbers(name)
    number = 0
    total = 0
    url_list = []
    while True:
        total = number * 50

        url = 'http://tieba.baidu.com/f?kw=' + name + '&pn=' + str(total)
        url_list.append(url)

        number += 1
        if number_tuple[2] - total < 50:
            break
    return url_list

#获取页面信息
def getresponse(url):
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

#获取帖子列表
def gettiezilist(name):
    url_list = gettiebalist(name)
    intro_url_list = []
    flag = 0
    for url in url_list:
        data = getresponse(url)
        div_redstr = '<li class=" j_thread_list clearfix" data-field=([\s\S]*?)<div class="threadlist_author pull_right">'
        div_regex = re.compile(div_redstr, re.IGNORECASE)
        # 帖子列表
        div_list = re.findall(div_regex, data)

        href_list = 'href="/p/(\d+)"'
        href_regex = re.compile(href_list, re.IGNORECASE)
        for div_str in div_list:
            href_list = re.findall(href_regex, div_str)
            print('-'*50)
            print(href_list)
            intro_url = 'http://tieba.baidu.com/p/' + href_list[0]
            intro_url_list.append(intro_url)
        #抓取前5页
        if flag > 5:
            break
        else :
            flag+=1
         #time.sleep(1)
    return intro_url_list

#获取友情贴吧
def getFriendshipBar(name):
    url = 'http://tieba.baidu.com/f?'
    word = {
            'kw': name,
            'pn': 0
            }
    word = parse.urlencode(word)
    url = url + word
    data = getresponse(url)

    friendReStr = 'kw=([\S\s]{0,10}?)&frs'
    friendshipRegex = re.compile(friendReStr,re.IGNORECASE)
    friendBarList = re.findall(friendshipRegex,data)
    friendBarList = list(set(friendBarList))
    if name in friendBarList:
        friendBarList.remove(name)
    return friendBarList
