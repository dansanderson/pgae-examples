import datetime
import webapp2
from google.appengine.api import urlfetch


class MainPage(webapp2.RequestHandler):
    def get(self):

        try:
            newsfeed = urlfetch.fetch('http://ae-book.appspot.com/blog/atom.xml',
                                      allow_truncated=False,
                                      follow_redirects=False,
                                      deadline=10)
            newsfeed_xml = newsfeed.content
        
            self.response.write('<p>Read PGAE blog feed (%d characters).</p>'
                                % len(newsfeed_xml))
            
        except urlfetch.Error, e:
            self.response.write('<p>urlfetch.Error: %s</p>' % e)
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))
        

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
