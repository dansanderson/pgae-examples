import datetime

counter = 0

def incr_and_print_counter():
    global counter
    counter += 1
    print '<p>Counter: %d</p>' % counter

print 'Content-Type: text/html'
print ''
print '''<p>This request handler does not have a main() method, and so is
evaluated fresh every time this page is loaded.  The global counter
does not increase because it is re-initialized each time the script
is evaluated.</p>

<ul>
  <li><a href="/">/</a></li>
  <li><a href="/cached">/cached</a></li>
</ul>
'''

incr_and_print_counter()

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
