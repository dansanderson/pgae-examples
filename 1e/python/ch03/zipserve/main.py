import datetime

print 'Content-Type: text/html'
print ''
print '<p><a href="/archive/somedir/somefile.txt">Go to a file served by zipserve.</a></p>'
print '<p>The time is: %s</p>' % str(datetime.datetime.now())
