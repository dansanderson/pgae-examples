import datetime
import os

print 'Content-Type: text/html'
print ''

if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    print ('<p>You are running on the development server.   You can use '
           '<a href="/_ah/admin/inboundmail">the development server console</a> '
           'to send email to this application.</p>')
else:
    app_email_address = 'support@' + os.environ['APPLICATION_ID'] + '.appspotmail.com'
    print ('<p>You are running on App Engine.  You can '
           '<a href="mailto:%s">send email to %s</a> to send a message '
           'to the application.</p>' % (app_email_address, app_email_address))

print '<p>This app will write to the log when it receives email messages.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
