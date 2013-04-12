import datetime
import os
import webapp2
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.response.write('<p>You are not signed in to Google Accounts. '
                                '<a href="%s">Sign in</a>.</p>'
                                % users.create_login_url(os.environ['PATH_INFO']))
        else:
            self.response.write('<p>You are signed in as %s. ' % user.nickname())
            if users.is_current_user_admin():
                self.response.write('You are an administrator. ')
            self.response.write('<a href="%s">Sign out</a>.</p>'
                                % users.create_logout_url('/'))

        self.response.write('''
<ul>
  <li><a href="/">/</a></li>
  <li><a href="/required">/required</a></li>
  <li><a href="/admin">/admin</a></li>
</ul>''')

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/.*', MainPage)], debug=True)
