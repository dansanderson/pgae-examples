from google.appengine.ext import db
import datetime
import webapp2

class Location(db.Model):
    name = db.StringProperty()

class GameObject(db.Model):
    name = db.StringProperty()
    location = db.ReferenceProperty(Location)

class CarryableObject(GameObject):
    weight = db.IntegerProperty()

class PourableObject(GameObject):
    contents = db.StringProperty()
    amount = db.IntegerProperty()

class Bottle(CarryableObject, PourableObject):
    is_closed = db.BooleanProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):

        here = Location(name='Upper Shore')
        here.put()
        
        bottle = Bottle(name='heavy jug',
                        location=here,
                        weight=125,
                        contents='apple juice',
                        amount=10,
                        is_closed=True)
        bottle.put()
        self.response.write('<p>Created a Bottle with inherited property '
                            'declarations.</p>')
        
        db.delete([here, bottle])
        self.response.write('<p>Entities deleted.</p>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
