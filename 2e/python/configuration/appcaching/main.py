import datetime
import webapp2

# An app instance global.
app_counter = 0

class MainPage(webapp2.RequestHandler):
    # A class variable.
    cls_counter = 0

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)

        # A handler instance variable.
        self.counter = 0

    def incr_and_print_counter(self):
        global app_counter

        app_counter += 1
        MainPage.cls_counter += 1
        self.counter += 1

        self.response.write('<p>App counter: %d</p>' % app_counter)
        self.response.write('<p>Class counter: %d</p>' % MainPage.cls_counter)
        self.response.write('<p>Object counter: %d</p>' % self.counter)

    def get(self):
        self.response.write('''
<p>This request handler accesses and modifies three counter variables: a module global, a class global, and an handler object member.  When App Engine starts a new instance for an app, its memory begins empty.  The first request handled by a request handler on the instance imports the <code>main</code> module, which initializes the module global and class global to zero (0).  App Engine constructs a new instance of the <code>MainPage</code> class for each request, which initializes its instance member counter.</p>

<p>When you reload this page, the module and class globals may change depending on which instance handles your request, and how many previous requests the instance has handled.  This number may fluctuate as new instances are started and requests are distributed across live instances.  The object counter remains at 1, because each request gets its own handler object.</p>
''')

        self.incr_and_print_counter()

        self.response.write('<p>The time is: %s</p>' % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
