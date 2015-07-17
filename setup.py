#!/usr/bin/env python

import os
import sys
import sqlite3 as sql
from Crypto.Hash import SHA256
from subprocess import call

db_path = 'db/'
db_sql = db_path + 'raspi-tv.sql'
db_sqlite = db_path + 'raspi-tv.sqlite'


def ask(text):
    answer = None
    while not answer:
        answer = raw_input(text)
    return answer


def sha256(data):
    return SHA256.new(data).hexdigest()


def create(action):
    assert len(action) == 1, 'Expecting only one argument.'
    action = action[0]
    actions = ['user', 'database']
    if action in actions:
        if action == actions[0]:
            assert os.path.isfile(db_sqlite), 'SQLite database not yet created.\n' \
                                              'Try executing: python setup.py create database'
            db = sql.connect(db_sqlite)
            user = ask('Username: ')
            while db.execute('SELECT COUNT(*) FROM Users WHERE UserId=?', (user,)).fetchone()[0]:
                print('User already exists. Please try again.')
                user = ask('Username: ')
            password = ''
            while True:
                password = ask('Password: ')
                if password == ask('Repeat the password: '):
                    break
                else:
                    print('Passwords don\' match. Please try again.')
            password = sha256(password)
            first_name = ask('First name: ')
            last_name = ask('Last name: ')
            email = ask('Email: ')
            db.execute('INSERT INTO Users VALUES (?, ?, ?, ?, ?)', (user, password, first_name, last_name, email))
            db.commit()
            db.close()
        elif action == actions[1]:
            call('cat ' + db_sql + ' | sqlite3 ' + db_sqlite, shell=True)


if __name__ == '__main__':
    functions = {'create': create}
    if sys.argv[1] in functions.keys():
        functions[sys.argv[1]](sys.argv[2:])
