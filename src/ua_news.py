import xmltodict
import urllib2
import feedparser

def deti_news():
    # obter atraves do url
    feed_content = feedparser.parse('http://services.web.ua.pt/deti/news/')

    news = {"title": feed_content.feed.title, "news": []}

    for entry in feed_content.entries:
        news["news"] += [{"author": entry.author,
                          "summary": entry.summary,
                          "title": entry.title,
                          "date": str(entry.updated)}]


    return news

if __name__ == '__main__':
    resp = deti_news()
    resp