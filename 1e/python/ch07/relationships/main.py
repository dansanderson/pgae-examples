from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Book(db.Model):
    title = db.StringProperty()
    author = db.StringProperty()
    previous_edition = db.SelfReferenceProperty()

class BookReview(db.Model):
    book = db.ReferenceProperty(Book, collection_name='reviews')

b = Book(title = 'The Grapes of Wrath',
         author = 'John Steinbeck')
b.put()

print '<p>Created a Book with key %s</p>' % b.key()

br = BookReview()
br.book = b        # sets br's 'book' property to b's key
br.book = b.key()  # same thing
br.put()

print '<p>Created a BookReview with key %s</p>' % br.key()

# ReferenceProperty declarations can do automatic de-referencing.
# This does a datastore fetch if necessary
print '<p>br\'s book\'s title is %s</p>' % br.book.title

b2 = Book()
br2 = BookReview()
try:
    br2.book = b2
except db.BadValueError, e:
    print '''<p>I cannot assign b2 to br2.book without saving b2 first.
b2\'s key is incomplete because it does not have a key name, and must be
saved to get a system ID before its key can be used as a reference.</p>'''

b2.put()
br2.book = b2
br2.put()
print '''<p>b2 has been saved, and its key can now be used as a reference.<p>'''

br2r2 = BookReview(book=b2)
br2r3 = BookReview(book=b2)
br2r4 = BookReview(book=b2)
db.put([br2r2, br2r3, br2r4])

# ReferenceProperty creates a special attribute on the referenced
# class that when accessed performs a query for objects of the
# referring class that refer to a given object.  The name of this
# attribute is set by "collection_name" in the ReferenceProperty
# declaration.  Accessing b2.reviews performs a datastore query for
# all BookReview entities whose "book" property is b2's key.
print '<p>b2 has these corresponding BookReviews:</p><ul>'
for review in b2.reviews:
    print '<li>%s</li>' % review.key()
print '</ul>'

# Using a self-reference property.
b3 = Book()
b3.previous_edition = b2
b3.put()

db.delete([b, br, b2, br2, br2r2, br2r3, br2r4, b3])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
