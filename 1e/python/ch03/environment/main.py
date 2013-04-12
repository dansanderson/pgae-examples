import cgi
import datetime
import os
import sys

print 'Content-Type: text/html'
print ''

print '<ul>'
print '<li><a href="#env">Environment Variables</a></li>'
print '<li><a href="#filesystem">File System</a></li>'
print '<li><a href="#request">Request Data</a></li>'
print '</ul>'

print '<hr noshade><h2 id="env">Environment Variables</h2><table>'
keys = os.environ.keys()
keys.sort()
for k in keys:
    print ('<tr><td valign="top"><code>%s</code></td><td valign="top"><code>%s</code></td></tr>'
           % (cgi.escape(k), cgi.escape(os.environ[k])))
print '</table>'

print '<hr noshade><h2 id="filesystem">File System</h2><pre>'
for path, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        print cgi.escape(os.path.join(path, filename))
print '</pre>'

print '<hr noshade><h2 id="request">Request Data</h2><pre>'
print cgi.escape(sys.stdin.read())
print '</pre>'

print '<hr noshade><p>The time is: %s</p>' % str(datetime.datetime.now())
