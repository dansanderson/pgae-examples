import datetime

counter = 0

def incr_and_print_counter():
    global counter
    counter += 1
    print '<p>Counter: %d</p>' % counter

def main():
    print 'Content-Type: text/html'
    print ''
    print '''<p>This request handler has a main() method, and so is
evaluated once per app instance.  When an instance is
re-used, the script is not re-evaluated and its main()
function is called.  The global counter increases when
the app is re-used.</p>

<p>You may need to refresh your browser multiple times
in quick succession to see the counter increase when
running on App Engine to get App Engine to re-use the
app.</p>

<ul>
  <li><a href="/">/</a></li>
  <li><a href="/cached">/cached</a></li>
</ul>
'''

    incr_and_print_counter()

    print '<p>The time is: %s</p>' % str(datetime.datetime.now())

if __name__ == '__main__':
    main()
