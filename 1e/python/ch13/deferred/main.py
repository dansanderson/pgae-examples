import datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import deferred
import invitation

class SendInvitationHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        recipient = users.get_current_user().email()
        deferred.defer(invitation.send_invitation, recipient)
        self.response.out.write('<p>Your invitation has been sent to your email address.</p>')

        self.response.out.write('<p>The time is: %s</p>'
                                % str(datetime.datetime.now()))

application = webapp.WSGIApplication([
    ('/', SendInvitationHandler),
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
