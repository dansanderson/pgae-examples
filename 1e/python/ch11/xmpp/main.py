import datetime
import os

print 'Content-Type: text/html'
print ''

app_id = os.environ['APPLICATION_ID']
version_id = os.environ['CURRENT_VERSION_ID']
version_id = version_id[:version_id.find('.')]

if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    print ('<p>You are running on the development server.   You can use '
           '<a href="/_ah/admin/xmpp">the development server console</a> '
           'to send an XMPP chat message to this application.</p>'
           '<p><i>Be sure to use <b>%s@appspot.com</b> or '
           '<b>anything@%s.appspotchat.com</b> as the "To" '
           'address.</i></p>' % (app_id, app_id))
else:
    app_xmpp_address = ('something@%s.latest.%s.appspotchat.com'
                        % (version_id, app_id))
    print ('<p>You are running on App Engine.  You can '
           'send an XMPP chat message to %s to communicate with '
           'this application.</p>' % app_xmpp_address)

print ('<p>This app responds to messages that contain simple '
       'two-term arithmetic expressions, such as <code>2 + 3</code> '
       'or <code>144 / 4</code>.</p>')

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
