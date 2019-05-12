import time
import sqlite3

db_path = 'D:\\wait_crawl.db'
email_db_path = 'D:\\tieba_email.db'

#保存邮箱数据到本地数据库
def save_email(list):
    conn = sqlite3.connect(email_db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS emails (email TEXT NOT NULL UNIQUE, date TEXT NOT NULL);")
    for email in list:
        c.execute("INSERT OR IGNORE INTO emails VALUES('" + email+ "','" + time.strftime('%Y%m%d',time.localtime(time.time())) +"');")
    conn.commit()
    conn.close()

#保存待爬取贴吧
def save_wait_crawl_bar(list):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS wait_crawl (name TEXT NOT NULL UNIQUE, isCrawled BOOL NOT NULL);")
    for bar_name in list:
       c.execute("INSERT OR IGNORE INTO wait_crawl VALUES('" + bar_name + "',0);")
    conn.commit()
    conn.close()

#获取待爬取贴吧
def get_uncrawled_bar():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cursor = c.execute("SELECT name FROM wait_crawl WHERE isCrawled = 0 ORDER BY RANDOM() limit 1")
    for row in cursor:
        name = row[0]
    conn.close()
    return name

#更改被爬贴吧
def update_crawl_bar(name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cursor = c.execute("UPDATE wait_crawl SET isCrawled = 1 WHERE name = '" + name +"'")
    conn.commit()
    conn.close()