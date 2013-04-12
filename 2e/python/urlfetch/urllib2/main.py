import datetime
import urllib2
import webapp2
from google.appengine.api import urlfetch

class MainPage(webapp2.RequestHandler):
    def get(self):

        try:
            newsfeed = urllib2.urlopen('http://ae-book.appspot.com/blog/atom.xml')
            newsfeed_xml = newsfeed.read()
        
            self.response.write('<p>Read PGAE blog feed (%d characters).</p>'
                                % len(newsfeed_xml))
            
        except urllib2.URLError, e:
            self.response.write('<p>urllib2.URLError: %s</p>' % e)
        
        except urlfetch.Error, e:
            self.response.write('<p>urlfetch.Error: %s</p>' % e)
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))
        

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
