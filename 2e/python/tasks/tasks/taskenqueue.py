import datetime
import os
import webapp2
from google.appengine.api import taskqueue

class MainPage(webapp2.RequestHandler):
    def get(self):

        taskqueue.add()
        taskqueue.add()
        taskqueue.add()
        self.response.write('<p>Enqueued 3 tasks to the default queue.</p>')
        
        taskqueue.add(url='/send_invitation_task',
                      params={'address': 'juliet@example.com',
                              'firstname': 'Juliet'})
        self.response.write(
            '<p>Enqueued 1 task to the default queue with parameters.</p>')
        
        if os.environ['SERVER_SOFTWARE'].startswith('Development'):
            self.response.write(
                '<p>This app is running in the development console.  Browse '
                'the server console output (the log) to '
                'verify the tasks have executed.</p>  <p>See also '
                '<a href="http://localhost:8080/_ah/admin/queues">'
                'the development console</a>.')
        else:
            self.response.write(
                '<p>This app is running on App Engine.  Browse the logs to '
                'verify the tasks have executed.</p>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
