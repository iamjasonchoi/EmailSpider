from urllib import parse
import string
import urllib.request
import re
import time
import crawl


def getmail(name):
    emailCount = 0
    mail_restr = r'([A-Za-z0-9_+]+@[A-Za-z0-9]+\.[A-Za-z]{2,6})'
    mail_dirty = r'(u[A-Fa-f0-9]{4}[A-Za-z0-9_+]+@[A-Za-z0-9]+\.[A-Za-z]{2,6})'
    mail_regex = re.compile(mail_restr, re.IGNORECASE)
    mail_dirty_regex = re.compile(mail_dirty,re.IGNORECASE)

    intro_url_list =  crawl.gettiezilist(name)
    for intro_url in intro_url_list:
        data = crawl.getresponse(intro_url)

        page_re_str = '共<span class="red">(\d+)</span>页</li>'
        page_re_gex = re.compile(page_re_str, re.IGNORECASE)
        page_re_list = []
        if data != None:
            try:
                page_re_list = re.findall(page_re_gex, data)
            except TypeError:
                page_re_list = re.findall(page_re_gex, data.decode())
            print(intro_url)
            print(page_re_list)
            if len(page_re_list) > 0:
                page = eval(page_re_list[0])
            else:
                print('帖子被隐藏，跳过')
                continue
        else:
            print('获取帖子失败')
            continue
        print(page)
        for i in range(page):

            print(i)
            page_url = intro_url + '?pn=' + str(i+1)
            print(page_url)
            data = crawl.getresponse(page_url)

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
                #保存到本地文件
                fileObject = open('D:\\email' + time.strftime('%Y%m%d',time.localtime(time.time())) + '.txt','a')
                for mail in mail_list:
                    fileObject.write(mail)
                    fileObject.write('\n')
                    emailCount += 1
                fileObject.close()
            time.sleep(2)
            print('当前有效邮箱爬取数：')
            print(emailCount)
            print('=' * 20)
    print('爬取结束')
    print(emailCount)


def main():
    while True:
        nameList = []
        #读取被爬贴吧
        with open('barName.txt','r') as f:
            for line in f:
                isExist = False
                with open('crawledBarName.txt','r') as crawledName:
                    for crawled in crawledName:
                        if line == crawled:
                            isExist = True
                            break
                if isExist:
                    continue

                barName = urllib.parse.quote(line.replace('\n',''))
                nameList = nameList + crawl.getFriendshipBar(line.replace('\n',''))
                getmail(barName)

                with open('crawledBarName.txt','a') as crawledName:
                    crawledName.write(line)
        #保存友情贴吧
        with open('barName.txt','a') as f:
            for name in nameList:
                f.write(name)
                f.write('\n')
            f.close()
        nameList.clear()



if __name__ == "__main__":
    main()

