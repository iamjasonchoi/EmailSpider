import Crawl
import EmailData

def main():
    name = "kindle"
    total_count = 0
    while True:
        EmailData.save_wait_crawl_bar(Crawl.get_friend_bar(name))
        total_count += Crawl.get_email(name)
        EmailData.update_crawl_bar(name)
        name = EmailData.get_uncrawled_bar()
        print("当前共获取邮箱数：" + str(total_count))


if __name__ == "__main__":
    main()
