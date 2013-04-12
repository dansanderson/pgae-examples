import datetime
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<p><a href="/archive/somedir/somefile.txt">'
                            'Go to a file served by zipserve.</a></p>')
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

