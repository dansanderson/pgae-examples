import datetime
import os

print 'Content-Type: text/html'
print ''

if os.environ.get('HTTPS') == 'on':
    print '<p>This page was accessed over a secure connection.</p>'
else:
    print '<p>This page was accessed over a normal (non-secure) connection.</p>'

server_name = os.environ.get('SERVER_NAME')
server_port = os.environ.get('SERVER_PORT')
is_dev_server = os.environ['SERVER_SOFTWARE'].startswith('Development')

print '<ul>'
if is_dev_server:
    for path in ('', 'always', 'never', 'optional'):
        url = 'http://%s:%s/%s' % (server_name, server_port, path)
        print '<li><a href="' + url + '">' + url + '</a></li>'
else:
    for scheme in ('http', 'https'):
        for path in ('', 'always', 'never', 'optional'):
            url = '%s://%s/%s' % (scheme, server_name, path)
            print '<li><a href="' + url + '">' + url + '</a></li>'
print '</ul>'

if is_dev_server:
    print '<p>The development server does not support HTTPS, only HTTP.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
