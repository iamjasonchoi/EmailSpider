import crawl
import string
import ioTool

def main():
    count = 0
    groups = crawl.getGroups('电子书')
    for group in groups:
        topics = crawl.GetTopics(group)
        for topic in topics:
            emails = crawl.get_emails(topic)
            if len(emails) > 0:
                ioTool.save_emails(emails)
                count = count + len(emails)
                print('当前爬取数:')
                print(count)
            print('='*40)
if __name__ == "__main__":
    main()
