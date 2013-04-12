from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Book(db.Expando):
    pass

# Creating an entity with a system ID
obj = Book()
obj.title = 'The Grapes of Wrath'
obj.author = 'John Steinbeck'
obj.copyright_year = 1939
obj.author_birthdate = datetime.datetime(1902, 2, 27)
obj.put()
print '<p>Created a Book entity, key = %s</p>' % obj.key()

# Initializing property values in the constructor
obj2 = Book(title='The Grapes of Wrath',
            author='John Steinbeck',
            copyright_year=1939,
            author_birthdate=datetime.datetime(1902, 2, 27))
obj2.put()
print '<p>Created a Book entity, key = %s</p>' % obj2.key()

# Creating an entity with a key name
obj3 = Book(key_name='0143039431',
            title='The Grapes of Wrath',
            author='John Steinbeck',
            copyright_year=1939,
            author_birthdate=datetime.datetime(1902, 2, 27))
obj3.put()
print '<p>Created a Book entity, key = %s</p>' % obj3.key()

# Using get_or_insert to create an entity with a key name
obj4 = Book.get_or_insert('0143039431')
if obj4.title:
    print '<p>Found Book with key name "0143039431", not creating a new one'
else:
    print '<p>Did not find a Book with key name "0143039431", creating a new one'
    obj4.put()

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
