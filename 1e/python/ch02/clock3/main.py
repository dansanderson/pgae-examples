from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime

class MainPage(webapp.RequestHandler):
    def get(self):
        time = datetime.datetime.now()
        user = users.get_current_user()
        if not user:
            navbar = ('<p>Welcome! <a href="%s">Sign in or register</a> to customize.</p>'
                      % (users.create_login_url(self.request.path)))
        else:
            navbar = ('<p>Welcome, %s! You can <a href="%s">sign out</a>.</p>'
                      % (user.email(), users.create_logout_url(self.request.path)))

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('''
        <html>
            <head>
                <title>The Time Is...</title>
            </head>
            <body>
            %s
                <p>The time is: %s</p>
            </body>
        </html> ''' % (navbar, str(time)))
        
application = webapp.WSGIApplication([('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
