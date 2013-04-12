import datetime

print 'Content-Type: text/html'
print ''

print ('<p>This application is configured with the remote '
       'API entry point at <code>/remote_api</code>.  See '
       '<code>web.xml</code> for the configuration, and see '
       'the <code>python/ch12/</code> directory for Python '
       'code that configures the bulk loader tools.</p>')

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
