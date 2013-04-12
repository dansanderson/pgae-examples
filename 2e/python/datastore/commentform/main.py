from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users
import cgi
import datetime
import webapp2

class Comment(db.Expando):
    pass

class CommentHandler(webapp2.RequestHandler):
    def post(self):
        c = Comment()
        c.commenter = users.get_current_user()
        c.message = db.Text(self.request.get('message'))
        c.date = datetime.datetime.now()
        c.put()

        self.redirect('/')

class CommentFormHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<p>Comments:</p><ul>')
        # Borrowing a bit from chapter 5...
        for c in Comment.all().order('-date'):
            self.response.out.write('<li>%s<br />posted by %s on %s</li>'
                                    % (cgi.escape(c.message),
                                       cgi.escape(c.commenter.nickname()),
                                       c.date))
        self.response.out.write('</ul>')

        self.response.out.write('''<p>Post a comment:</p>
<form action="/post" method="POST">
<textarea name="message"></textarea><br />
<input type="submit" />
</form>
''')

app = webapp2.WSGIApplication(
    [('/', CommentFormHandler),
     ('/post', CommentHandler)],
    debug=True)
