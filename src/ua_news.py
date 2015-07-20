import xmltodict
import urllib2
import feedparser

def deti_news():
    # obter atraves do url
    feed_content = feedparser.parse('http://services.web.ua.pt/deti/news/')

    return feed_content

if __name__ == '__main__':
    deti_news()
