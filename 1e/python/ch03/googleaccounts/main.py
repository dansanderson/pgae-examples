import datetime
import os
from google.appengine.api import users

print 'Content-Type: text/html'
print ''

user = users.get_current_user()
if not user:
    print '<p>You are not signed in to Google Accounts. '
    print '<a href="%s">Sign in</a>.</p>' % users.create_login_url(os.environ['PATH_INFO'])
else:
    print '<p>You are signed in as %s. ' % user.nickname()
    if users.is_current_user_admin():
        print 'You are an administrator. '
    print '<a href="%s">Sign out</a>.</p>' % users.create_logout_url('/')

print '<ul>'
print '<li><a href="/">/</a></li>'
print '<li><a href="/required">/required</a></li>'
print '<li><a href="/admin">/admin</a></li>'
print '</ul>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
