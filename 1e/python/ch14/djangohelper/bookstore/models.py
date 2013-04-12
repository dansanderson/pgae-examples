from appengine_django.models import BaseModel
from google.appengine.ext import db
from django import test
import datetime

class Book(BaseModel):
    title = db.StringProperty(verbose_name='Book title')
    author = db.StringProperty()
    copyright_year = db.IntegerProperty()
    author_birthdate = db.DateProperty()

class BookReview(BaseModel):
    book = db.ReferenceProperty(Book, collection_name='reviews')
    review_author = db.UserProperty()
    review_text = db.TextProperty()
    rating = db.StringProperty(choices=['Poor', 'OK', 'Good', 'Very Good', 'Great'],
                               default='Great')
    create_date = db.DateTimeProperty(auto_now_add=True)

class TestBook(test.TestCase):
    def setUp(self):
        self.book = Book(title='test title',
                         author='test author',
                         copyright_year=1922,
                         author_birthdate=datetime.date(1900, 1, 1))

    def testCreateDate(self):
        self.assert_(self.book.author_birthdate
                     and isinstance(self.book.author_birthdate, datetime.date))

    def testAuthorMustBeAString(self):
        def badAssignment():
            self.book.author = 999
        self.assertRaises(db.BadValueError,
                         badAssignment)

    def testAuthorIsAString(self):
        self.book.author = 'Steinbeck, John'

class TestBooksAndReviews(test.TestCase):
    fixtures = ['bookstore.json']

    def testBookReviewOrder(self):
        d = Book.all().filter('title =', 'one').get()
        self.assert_(d, 'Book "one" must be in test fixture')

        q = BookReview.all().filter('book =', d)
        q.order('-create_date')
        reviews = q.fetch(3)
        self.assertEqual('review3', reviews[0].review_text)
        self.assertEqual('review2', reviews[1].review_text)
        self.assertEqual('review1', reviews[2].review_text)
