import datetime
import os
from google.appengine.api.labs import taskqueue

print 'Content-Type: text/html'
print ''

taskqueue.add()
taskqueue.add()
taskqueue.add()
print '<p>Enqueued 3 tasks to the default queue.</p>'

taskqueue.add(url='/send_invitation_task',
              params={'address': 'juliet@example.com',
                      'firstname': 'Juliet'})
print '<p>Enqueued 1 task to the default queue with parameters.</p>'

if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    print '<p>This app is running in the development console.  See <a href="http://localhost:8080/_ah/admin/queues">the development console</a> to browse and execute tasks.'
else:
    print '<p>This app is running on App Engine.  Browse the logs to verify the tasks have executed.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
