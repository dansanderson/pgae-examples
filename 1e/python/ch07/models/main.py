from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Book(db.Model):
    title = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    copyright_year = db.IntegerProperty()
    author_birthdate = db.DateProperty()

obj = Book(title='The Grapes of Wrath',
           author='John Steinbeck')
obj.copyright_year = 1939
obj.author_birthdate = datetime.date(1902, 2, 27)

try:
    obj.copyright_year = 'not a number'
except db.BadValueError, e:
    print '<p>I cannot assign a str to a property declared with db.IntegerProperty.</p>'

try:
    obj.author_birthdate = datetime.datetime.now()
except db.BadValueError, e:
    print '''<p>I cannot assign a datetime.datetime to a property declared
with db.DateProperty, which accepts a datetime.date.  The db.DateProperty
class converts datetime.date values to and from the datastore native type
datetime.datetime for storage.</p>'''

try:
    obj2 = Book(title='Authorless Book')
except db.BadValueError, e:
    print '<p>I cannot create a Book without initializing the required author property.</p>'

try:
    obj.author = None
except db.BadValueError, e:
    print '<p>I cannot assign None to a property declared as required.</p>'

obj.copyright_year = None
print '<p>But I can assign None to a property not declared as required.</p>'

try:
    obj.new_prop = 12345
except db.BadValueError, e:
    print '''<p>With a model class derived from db.Model, I cannot assign
values to properties that have not been declared. If the model class uses
the db.Expando base class, the class can declare properties and also accept
values for undeclared properties.</p>'''

obj.put()
print '<p>Saved the entity.</p>'
db.delete(obj)
print '<p>Deleted the entity.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
