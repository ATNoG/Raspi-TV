import feedparser
import urllib
import sqlite3 as sql

def deti_news():
    feed_content = feedparser.parse('http://services.web.ua.pt/deti/news/')

    news = {"title": feed_content.feed.title, "news": []}
    db = sql.connect('../db/raspi-tv.sqlite')

    for entry in feed_content.entries:
        news["news"] += [{"author": parse_author(entry.author),
                          "summary": entry.summary,
                          "title": entry.title,
                          "date": parse_date(str(entry.updated))}]

    print news["news"][0]["title"]
    for i in range(0, len(news["news"])):
        db.execute("INSERT INTO News VALUES (?,?,?,?);",
                   (news["news"][i]["title"], news["news"][i]["date"], news["news"][i]["author"], news["news"][i]["summary"]))
        db.commit()
    db.close()

    return news


def parse_author(author):
    if "=?iso-8859-1?Q?" in author:
        slices = urllib.unquote(author.replace("=", "%").replace("\"", "")).replace("?%", "").split("%?iso-8859-1?Q?")
        author = ""
        for slice in slices:
            author += slice.strip().replace("_", " ")
    return author

def parse_date(date):

    date_time = date.split("T")
    tmp = date_time[1].split("+")
    return " Date: " + date_time[0] + " Hour: " + tmp[0]


if __name__ == '__main__':
    resp = deti_news()
    resp