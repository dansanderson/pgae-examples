import datetime
import webapp2
from google.appengine.api import users
from google.appengine.ext import deferred
import invitation

class SendInvitationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        recipient = users.get_current_user().email()
        deferred.defer(invitation.send_invitation, recipient)
        self.response.write('<p>Your invitation has been sent to your email address.</p>')

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))

app = webapp2.WSGIApplication([
    ('/', SendInvitationHandler),
    ], debug=True)
