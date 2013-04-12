import jinja2
import os
import webapp2

from google.appengine.ext import db

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()))

PAGE_SIZE = 10

class Message(db.Model):
    create_date = db.DateTimeProperty(auto_now_add=True)
    # ...

class ResultsPageHandler(webapp2.RequestHandler):
    def get(self):
        query = Message.all().order('-create_date')
        cursor = self.request.get('c', None)
        if cursor:
            query.with_cursor(cursor)
        results = query.fetch(PAGE_SIZE)

        new_cursor = query.cursor()
        query.with_cursor(new_cursor)
        has_more_results = query.count(1) == 1

        template = template_env.get_template('results.html')
        context = {
            'results': results,
            }
        if has_more_results:
            context['next_cursor'] = new_cursor
        self.response.out.write(template.render(context))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('''
<form action="/" method="post">
<input type="submit" value="Create 12 Messages" />
</form>''')

    def post(self):
        for x in xrange(12):
            Message().put()
        self.redirect('/results')


app = webapp2.WSGIApplication([('/results', ResultsPageHandler),
                               ('/', MainPage)], debug=True)
