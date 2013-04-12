import datetime
import time
import webapp2
from google.appengine.api import urlfetch


class MainPage(webapp2.RequestHandler):
    def get(self):

        try:
            rpc = urlfetch.create_rpc()
            urlfetch.make_fetch_call(
                rpc,
                'http://ae-book.appspot.com/blog/atom.xml')
        
            # Do other things.
            time.sleep(2)
        
            newsfeed = rpc.get_result()
            newsfeed_xml = newsfeed.content
        
            self.response.write('<p>Read PGAE blog feed (%d characters).</p>'
                                % len(newsfeed_xml))
            
        except urlfetch.Error, e:
            self.response.write('<p>urlfetch.Error: %s</p>' % e)
        
        self.response.write('''
        <p>Try these:</p>
        <ul>
          <li><a href="/">a simple async call</a></li>
          <li><a href="/callbackobj">using a callback object</a></li>
          <li><a href="/callbackfunc">using a callback function</a></li>
        </ul>
        ''')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
