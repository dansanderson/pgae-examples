from google.appengine.ext import db
import datetime
import webapp2

class Book(db.Expando):
    pass

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Creating an entity with a system ID
        obj = Book()
        obj.title = 'The Grapes of Wrath'
        obj.author = 'John Steinbeck'
        obj.copyright_year = 1939
        obj.author_birthdate = datetime.datetime(1902, 2, 27)
        obj.put()
        self.response.write('<p>Created a Book entity, key = %s</p>'
                            % obj.key())
        
        # Initializing property values in the constructor
        obj2 = Book(title='The Grapes of Wrath',
                    author='John Steinbeck',
                    copyright_year=1939,
                    author_birthdate=datetime.datetime(1902, 2, 27))
        obj2.put()
        self.response.write('<p>Created a Book entity, key = %s</p>'
                            % obj2.key())
        
        # Creating an entity with a key name
        obj3 = Book(key_name='0143039431',
                    title='The Grapes of Wrath',
                    author='John Steinbeck',
                    copyright_year=1939,
                    author_birthdate=datetime.datetime(1902, 2, 27))
        obj3.put()
        self.response.write('<p>Created a Book entity, key = %s</p>'
                            % obj3.key())
        
        # Using get_or_insert to create an entity with a key name
        obj4 = Book.get_or_insert('0143039431')
        if obj4.title:
            self.response.write('<p>Found Book with key name "0143039431", '
                                'not creating a new one')
        else:
            self.response.write('<p>Did not find a Book with key name '
                                '"0143039431", creating a new one')
            obj4.put()
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
