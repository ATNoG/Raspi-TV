import feedparser
import urllib


def deti_news():
    feed_content = feedparser.parse('http://services.web.ua.pt/deti/news/')

    news = {"title": feed_content.feed.title, "news": []}

    for entry in feed_content.entries:
        news["news"] += [{"author": parse_author(entry.author),
                          "summary": entry.summary,
                          "title": entry.title,
                          "date": str(entry.updated)}]
    return news


def parse_author(author):
    if "=?iso-8859-1?Q?" in author:
        slices = urllib.unquote(author.replace("=", "%").replace("\"", "")).replace("?%", "").split("%?iso-8859-1?Q?")
        author = ""
        for slice in slices:
            author += slice.strip().replace("_", " ")
    return author


if __name__ == '__main__':
    resp = deti_news()
    resp