from google.appengine.ext import db
import datetime
import webapp2

class Entity(db.Expando):
    pass

class MainPage(webapp2.RequestHandler):
    def get(self):
        ids = db.allocate_ids(db.Key.from_path('Entity', 1), 1)
        e1_key = db.Key.from_path('Entity', ids[0])
        e1 = Entity(key=e1_key)
        e2 = Entity()
        e2.reference = e1_key

        db.put([e1, e2])

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
