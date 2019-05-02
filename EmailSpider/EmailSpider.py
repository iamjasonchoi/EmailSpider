from urllib import parse
import string
import urllib.request
import re
import time
import crawl


def getmail(name):
    emailCount = 0
    mail_restr = r'([A-Z0-9_+]+@[A-Z0-9]+\.[A-Z]{2,6})'
    mail_regex = re.compile(mail_restr, re.IGNORECASE)
    intro_url_list =  crawl.gettiezilist(name)
    for intro_url in intro_url_list:
        data = crawl.getresponse(intro_url)
        '''
        去一共几页
        '''
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
            try:
                mail_list = re.findall(mail_regex, data)
            except TypeError:
                mail_list = re.findall(mail_regex, data.decode())
            if len(mail_list) > 0:
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
    barName = urllib.parse.quote("考研资料")
    getmail(barName)


if __name__ == "__main__":
    main()

