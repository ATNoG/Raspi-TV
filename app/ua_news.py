import glob
import random
import string
import urllib

import feedparser
import os
import re
import wget
from constants import conn, ROOT_DIR


def deti_news():
    try:
        feed_source = conn.execute('SELECT * FROM HTMLSettings WHERE IdName=?', ('feed',)).fetchone()[1]
        feed_content = feedparser.parse(feed_source)

        news = {"title": feed_content.feed.title, "news": []}

        # delete all the images

        files = glob.glob(os.path.join(ROOT_DIR, 'public/img/feed_imgs/') + '*')
        for f in files:
            os.remove(f)

        conn.execute("DELETE FROM News;")

        for entry in feed_content.entries:
            news['news'] += [{'author': parse_author(entry.author) if hasattr(entry, 'author') else '',
                              'summary': entry.summary if hasattr(entry, 'summary') else '',
                              'title': entry.title if hasattr(entry, 'title') else '',
                              'date': parse_date(str(entry.updated)) if hasattr(entry, 'entry.updated') else ''}]

        for i in range(len(news['news'])):
            tmp = news["news"][i]['summary']
            new_tmp = download_photo(tmp)

            # try to clean...
            new_tmp = new_tmp.replace('<p class="MsoNormal"></p>', '')
            new_tmp = new_tmp.replace('<p></p>', '')
            new_tmp = new_tmp.replace('<br>', '')
            new_tmp = new_tmp.replace('<br />', '')
            new_tmp = new_tmp.replace('<p>&nbsp;</p>', '')

            # news without images
            tmp = tmp.replace('<p class="MsoNormal"></p>', '')
            tmp = tmp.replace('<p></p>', '')
            tmp = tmp.replace('<br>', '')
            tmp = tmp.replace('<br />', '')
            tmp = tmp.replace('<p>&nbsp;</p>', '')

            spaces = re.findall('(<p[^>]*><p[^>]*>.</p></p>&#13;)', new_tmp)
            for space in spaces:
                new_tmp = new_tmp.replace(space, "")
                tmp = tmp.replace(space, "")

            if new_tmp:
                conn.execute('INSERT INTO News (Title, Date_Updated, Author, Content) VALUES (?,?,?,?);',
                             (news['news'][i]['title'], news['news'][i]['date'], news['news'][i]['author'], new_tmp))
                conn.commit()
            else:
                conn.execute('INSERT INTO News (Title, Date_Updated, Author, Content) VALUES (?,?,?,?);',
                             (news['news'][i]['title'], news['news'][i]['date'], news['news'][i]['author'], tmp))
                conn.commit()
    except Exception, e:
        print e.message

    news_db = []

    for i in conn.execute('SELECT * FROM News;').fetchall():
        news_db.append({'author': i[3], 'summary': i[4], 'title': i[1], 'date': i[2]})

    return news_db


def parse_author(author):
    if '=?iso-8859-1?Q?' in author:
        slices = urllib.unquote(author.replace('=', '%').replace('"', '')).replace('?%', '').split("%?iso-8859-1?Q?")
        author = ""
        for slice in slices:
            author += slice.strip().replace("_", " ")
    return author


def parse_date(date):
    date_time = date.split('T')
    tmp = date_time[1].split('+')
    return ' Date: ' + date_time[0] + ' Hour: ' + tmp[0]


def download_photo(tmp):
    images = re.findall('(<img[^>]*src="[^"]*"[^>]*>)', tmp)

    for image in images:
        url = re.search('(src="[^"]*")', image)
        url = url.group(0)
        url = url.split("\"")[1]

        if 'cid' in url:
            tmp = tmp.replace(image, '')
        else:
            name = ''.join(random.choice(string.ascii_uppercase) for i in range(12))

            print name

            filename = wget.download(url, os.path.join(ROOT_DIR, 'public/img/feed_imgs/') + name + '.jpg')

            new_path_url = [filename, url]
            img_idx = new_path_url[0].find('img')
            tmp = tmp.replace(new_path_url[1], new_path_url[0][img_idx:])
    return tmp


if __name__ == '__main__':
    resp = deti_news()
