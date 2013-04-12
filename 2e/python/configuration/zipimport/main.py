import sys
sys.path.insert(0, 'packages.zip')

import datetime
import webapp2
from bigpackage import bigmodule

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(bigmodule.get_message())

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
