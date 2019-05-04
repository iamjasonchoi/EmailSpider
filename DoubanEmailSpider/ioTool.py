import time
import string

def save_emails(data):
    with open('e:\\douban_email_' + time.strftime('%Y%m%d',time.localtime(time.time())) + '.txt','a') as fileObject:
        for mail in data:
            fileObject.write(mail)
            fileObject.write('\n')
        fileObject.close()


