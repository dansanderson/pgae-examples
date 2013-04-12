import datetime
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):

        self.response.write('''
<p>This application is configured with the remote
API entry point at <code>/_ah/remote_api</code>.  See
<code>app.yaml</code> for the configuration.</p>
''')

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
