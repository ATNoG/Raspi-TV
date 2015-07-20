import xmltodict
import urllib2

def deti_news():
    # obter atraves do url
    feed_content = urllib2.urlopen('http://services.web.ua.pt/deti/news/')
    # fazer o parse do xml para um dicionario
    feed_object = xmltodict.parse(feed_content.read())

    print feed_object

    return feed_object

if __name__ == '__main__':
    deti_news()
