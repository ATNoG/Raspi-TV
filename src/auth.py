# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#

import cherrypy
from cgi import escape
from Crypto.Hash import SHA256
import sqlite3 as sql
import os
from settings import *

SESSION_KEY = '_cp_username'
conn = sql.connect(os.path.join(BASE_DIR, 'db/raspi-tv.sqlite'), check_same_thread=False)


def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    username = escape(username, True)
    u_pass = conn.execute('SELECT Password FROM Users WHERE UserId=?', (username,)).fetchone()
    if not u_pass:
        return 'Username ' + username + ' is unknown to me.'
    elif u_pass[0] != SHA256.new(password).hexdigest():
        return 'Incorrect password.'


def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/auth/login")
        else:
            raise cherrypy.HTTPRedirect("/auth/login")


cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)


def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""

    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f

    return decorate


# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

def member_of(groupname):
    def check():
        # replace with actual check if <username> is in <groupname>
        for user in conn.execute('SELECT UserId FROM Users'):
            if cherrypy.request.login == user[0] and groupname == 'admin':
                return True
        return False

    return check


def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login


# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""

    def check():
        for c in conditions:
            if c():
                return True
        return False

    return check


# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""

    def check():
        for c in conditions:
            if not c():
                return False
        return True

    return check


# Controller to provide login and logout actions

class AuthController(object):
    def on_login(self, username):
        """Called on successful login"""

    def on_logout(self, username):
        """Called on logout"""

    def get_loginform(self, username, msg="Enter login information", from_page='/admin'):
        username = escape(username, True)
        msg = escape(msg, True)
        from_page = escape(from_page, True)
        return open(os.path.join(BASE_DIR, 'src/static/admin/login.html')).read() % {'msg': msg, 'username': username}

    @cherrypy.expose
    def login(self, username=None, password=None, from_page='/admin'):
        if username is None or password is None:
            return self.get_loginform('', from_page=from_page)

        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or '/admin')

    @cherrypy.expose
    def logout(self, from_page='/'):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or '/')
