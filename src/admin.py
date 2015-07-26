import datetime
import sqlite3 as sql
import json

import cherrypy

from auth import require

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)


@require()
class Admin:
    def __init__(self):
        self.create = Create()
        self.get = Get()


class Create:
    def __init__(self):
        pass

    @cherrypy.expose
    def dropbox(self, account, token, note):
        date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        service = 'dropbox'
        if conn.execute('SELECT COUNT(*) FROM Accounts WHERE AccountId=? AND Service=?', (account, service)).fetchone()[
            0]:
            rtn = 'Unsuccessful. Account already exists.'
        else:
            conn.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)', (account, token, date, note, service))
            conn.commit()
            rtn = 'Successful.'
        return rtn

    @cherrypy.expose
    def twitter(self, account, token, note):
        date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        service = 'twitter'
        rtn = ''
        if conn.execute('SELECT COUNT(*) FROM Accounts WHERE AccountId=? AND Service=?', (account, service)).fetchone()[
            0]:
            rtn = 'Unsuccessful. Account already exists.'
        else:
            if conn.execute('SELECT COUNT(*) FROM Accounts WHERE Service=?', (service,)).fetchone()[0]:
                rtn = 'Warning: Only the first Twitter account of the database will be used for authentication.\n'
            conn.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)', (account, token, date, note, service))
            conn.commit()
            rtn += 'Successful.'
        return rtn


class Get:
    def __init__(self):
        pass

    @cherrypy.expose
    def dropbox(self):
        return self.get_service('dropbox')

    @cherrypy.expose
    def twitter(self):
        return self.get_service('twitter')

    def get_service(self, service):
        accounts = conn.execute('SELECT * FROM Accounts WHERE Service=?', (service,))
        rtn = []
        for account in accounts:
            rtn.append({'account': account[0], 'token': 'X' * len(account[1][:-4]) + account[1][-4:],
                        'date': account[2], 'note': account[3]})
        return json.dumps(rtn, separators=(',', ':'))
