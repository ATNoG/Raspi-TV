#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import sqlite3 as sql
from Crypto.Hash import SHA256
from subprocess import call
import getpass
import datetime

db_path = 'db/'
db_sql = db_path + 'raspi-tv.sql'
db_sqlite = db_path + 'raspi-tv.sqlite'


def ask(text, opt=0):
    answer = None
    if not opt:
        while not answer:
            answer = raw_input(text)
    elif opt == 1:
        while not answer:
            answer = getpass.getpass(text)
    return answer


def sha256(data):
    return SHA256.new(data).hexdigest()


def verify_db(rtn=False):
    if not rtn:
        assert os.path.isfile(db_sqlite), 'SQLite database not yet created.\n' \
                                          'Try executing: python setup.py create database'
    else:
        return os.path.isfile(db_sqlite)


def create(predicate):
    available_actions = ['user', 'database', 'cronjobs']
    assert len(predicate), 'Expecting a predicate:\n ' \
                           '' + repr(available_actions)
    action = predicate[0]
    if action in available_actions:
        if action == available_actions[0]:
            verify_db()
            db = sql.connect(db_sqlite)
            user = ''
            if len(predicate) == 2:
                user = predicate[1]
            elif len(predicate) > 2:
                print(' '.join(predicate[1:]) + ' is not a valid username. Consider quoting it.', file=sys.stderr)
                exit()
            else:
                user = ask('Username: ')
            while db.execute('SELECT COUNT(*) FROM Users WHERE UserId=?', (user,)).fetchone()[0]:
                print('User already exists. Please try again.')
                user = ask('Username: ')
            password = ''
            while True:
                password = ask('Password: ', opt=1)
                if password == ask('Repeat the password: ', opt=1):
                    break
                else:
                    print('Passwords don\' match. Please try again.')
            password = sha256(password)
            first_name = ask('First name: ')
            last_name = ask('Last name: ')
            email = ask('Email: ')
            date = datetime.datetime.now().strftime("%B %d, %Y")
            db.execute('INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?)',
                       (user, password, first_name, last_name, email, date))
            db.commit()
            db.close()
        elif action == available_actions[1]:
            if verify_db(rtn=True):
                print('This action will clear all the records currently on the database.')
                print('Continue?', end=' ')
                answer = ask('(Y/N) ').lower()
                while answer != 'y' and answer != 'n':
                    answer = ask('(Y/N) ').lower()
                if answer == 'n':
                    print('No changes were made.')
                    exit(0)
            call('cat ' + db_sql + ' | sqlite3 ' + db_sqlite, shell=True)

        elif action == available_actions[2]:
            cron_tasks = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/cron.py')
            print('Copy: \n')
            print('0 * * * * ' + ' python ' + str(cron_tasks))
            print('@reboot python /home/pi/Raspi-TV/src/web.py &')
            print('\nNow type \'crontab -e\' and at the bottom of the opened file paste the copied tasks.')


def delete(user):
    verify_db()
    if len(user) == 1:
        user = user[0]
    elif len(user) > 1:
        print(user + ' is not a valid username. Consider quoting it.', file=sys.stderr)
        exit(1)
    else:
        user = ask('Username: ')
    conn = sql.connect(db_sqlite)
    c = conn.cursor()
    c.execute('DELETE FROM Users WHERE UserId=?', (user,))
    if c.rowcount:
        conn.commit()
        conn.close()
        print('Successfully deleted user: ' + user)
    else:
        print(user + ' was not found.', file=sys.stderr)

if __name__ == '__main__':
    functions = {'create': create, 'delete': delete}
    if sys.argv[1] in functions.keys():
        functions[sys.argv[1]](sys.argv[2:])
