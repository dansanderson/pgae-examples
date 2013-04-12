import datetime
import os

print 'Content-Type: text/html'
print ''
print '''
<p>The following files and directories are in the app's
root directory on the application server:</p>

<pre>'''
print '\n'.join(os.listdir('.'))
print '''</pre>

<p>The "static" directory appears in this list in the
development server, but not when running on App Engine.</p>

<p>Links to static files:</p>

<ul>
  <li><a href="staticexpires.txt">staticexpires.txt</a> (text)</li>
  <li><a href="static/statictext.txt">static/statictext.txt</a> (text)</li>
  <li><a href="static/statictext.xxx">static/statictext.xxx</a> (text)</li>
  <li><a href="static/staticdownload.yyy">static/staticdownload.yyy</a> (download)</li>
</ul>
'''

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
