from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Book(db.Model):
    title = db.StringProperty()
    author = db.StringProperty()
    copyright_year = db.IntegerProperty()
    author_birthdate = db.DateProperty()

obj = Book()
obj.title = 'The Grapes of Wrath'
obj.author = 'John Steinbeck'
obj.copyright_year = 1939

# The DateProperty declaration accepts a datetime.date value, not a
# datetime.datetime value.
obj.author_birthdate = datetime.date(1902, 2, 27)

# Because the Book class is a subclass of db.Model, only the
# properties declared in the model can be assigned values, and those
# values must be of the declared types.  This would result in a
# runtime error:
#   obj.another_prop = 99
# So would this:
#   obj.author_birthdate = 'not a date'

obj.put()

print '<p>Created a Book entity, key = %s</p>' % obj.key()

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
