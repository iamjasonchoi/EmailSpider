from urllib import parse
import urllib.request
import re
import time
import EmailData

#获取贴吧分页url列表，每页50个帖子
def get_page_url_list(name):
    count = get_post_count(name)
    number = 0
    total = 0
    url_list = []
    while True:
        total = number * 50

        url = 'http://tieba.baidu.com/f?kw=' + name + '&pn=' + str(total)
        url_list.append(url)

        number += 1
        #最多获取每个贴吧前15页内容
        if count - total < 50 or total > 700:
            break
    return url_list

#获取贴吧帖子数
def get_post_count(name):
    url = 'http://tieba.baidu.com/f?'
    word = {
            'kw': name,
            'pn': 0
            }
    word = parse.urlencode(word)
    url = url + word
    data = get_response(url)
    count_rester = '共有主题数<span class="red_text">([\s\S]*?)</span>个'
    count_regex = re.compile(count_rester, re.IGNORECASE)
    count_list = re.findall(count_regex, data)
    post_number = 0
    if len(count_list):
        post_number = eval(count_list[0].replace(',', ''))
    return post_number

#获取友情贴吧列表
def get_friend_bar(name):
    url = 'http://tieba.baidu.com/f?'
    word = {
            'kw': name,
            'pn': 0
            }
    word = parse.urlencode(word)
    url = url + word
    data = get_response(url)

    friendReStr = 'kw=([\S\s]{0,10}?)&frs'
    friendshipRegex = re.compile(friendReStr,re.IGNORECASE)
    friendBarList = re.findall(friendshipRegex,data)
    friendBarList = list(set(friendBarList))
    if name in friendBarList:
        friendBarList.remove(name)
    return friendBarList

#根据吧名获取帖子列表
def get_post_url_list(name):
    url_list = get_page_url_list(name)
    post_url_list = []
    for url in url_list:
        data = get_response(url)
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
            post_url = 'http://tieba.baidu.com/p/' + href_list[0]
            post_url_list.append(post_url)
    str = len(post_url_list)
    return post_url_list

#获取页面信息
def get_response(url):
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

#获取邮箱
def get_email(real_name):
    name = urllib.parse.quote(real_name.replace('\n',''))
    total_email_count = 0
    mail_restr = r'([A-Za-z0-9_+]+@[A-Za-z0-9]+\.[A-Za-z]{2,6})'
    mail_dirty = r'(u[A-Fa-f0-9]{4}[A-Za-z0-9_+]+@[A-Za-z0-9]+\.[A-Za-z]{2,6})'
    mail_regex = re.compile(mail_restr, re.IGNORECASE)
    mail_dirty_regex = re.compile(mail_dirty,re.IGNORECASE)

    post_url_list = get_post_url_list(name)
    page = 0
    for url in post_url_list:
        page+=1
        if page > 50 and total_email_count <100:
            print("本帖吧无爬取价值，退出爬取")
            break;

        data = get_response(url)
        post_page_re_str = '共<span class="red">(\d+)</span>页</li>'
        post_page_re_gex = re.compile(post_page_re_str, re.IGNORECASE)
        #获取帖子回复页数
        post_page_total = 0
        if data != None:
            totals = []
            try:
                totals = re.findall(post_page_re_gex,data)
            except TypeError:
                totals = re.findall(page_re_gex, data.decode())
            if len(totals) > 0:
                post_page_total = eval(totals[0])
            print(url)
        else:
            print("获取帖子失败")
            continue
        print( "共" + str(post_page_total) + "页")
        post_count = 0
        for index in range(post_page_total):
            print("第" + str(index + 1) + "页:")
            page_url = url + '?pn=' + str(index+1)
            print(page_url)
            data = get_response(page_url)
            mail_list = []
            dirty_list = []
            try:
                mail_list = re.findall(mail_regex, data)
                dirty_list = re.findall(mail_dirty_regex,data)
            except TypeError:
                mail_list = re.findall(mail_regex, data.decode())
                dirty_list = re.findall(mail_dirty_regex,data.decode())
            if len(mail_list) > 0:
                if len(dirty_list) > 0:
                    for i in dirty_list:
                        if i in mail_list:
                            mail_list.remove(i)
                mail_list = list(set(mail_list))
                print(mail_list)
                total_email_count += len(mail_list)
                post_count += len(mail_list)
                #保存数据
                EmailData.save_email(mail_list)
            time.sleep(2)
            print(real_name + "吧—当前有效邮箱爬取数：" + str(total_email_count))
            #如果爬取超过5页且数目小于20，则认为是无效帖
            if index > 5 and post_count < 20:
                print("无价值帖，退出爬取")
                break
            print('=' * 40)
    return total_email_count

