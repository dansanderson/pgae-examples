import datetime
import os
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('''
<p>The following files and directories are in the app's
root directory on the application server:</p>

<pre>''')
        self.response.write('\n'.join(os.listdir('.')))
        self.response.write('''</pre>

<p>The "static" directory appears in this list in the
development server, but not when running on App Engine.</p>

<p>Links to static files:</p>

<ul>
  <li><a href="staticexpires.txt">staticexpires.txt</a> (text)</li>
  <li><a href="static/statictext.txt">static/statictext.txt</a> (text)</li>
  <li><a href="static/statictext.xxx">static/statictext.xxx</a> (text)</li>
  <li><a href="static/staticdownload.yyy">static/staticdownload.yyy</a> (download)</li>
</ul>
''')

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
