from google.appengine.ext import db
from google.appengine.ext.db import polymodel
import datetime
import webapp2

class Location(db.Model):
    name = db.StringProperty()

class GameObject(polymodel.PolyModel):
    name = db.StringProperty()
    location = db.ReferenceProperty(Location)

class CarryableObject(GameObject):
    weight = db.IntegerProperty()

class PourableObject(GameObject):
    contents = db.StringProperty()
    amount = db.IntegerProperty()

class Bottle(CarryableObject, PourableObject):
    is_closed = db.BooleanProperty()

class MusicalInstrument(CarryableObject):
    def play(self, handler):
        handler.response.write(
            '<p>You play the %s.  Everyone is impressed!</p>' % self.name)


class MainPage(webapp2.RequestHandler):
    def get(self):

        # Create some test data.
        here = Location(name='Upper Shore')
        here.put()
        location_key = here.key()
        
        bottle = Bottle(name='heavy jug',
                        location=here,
                        weight=125,
                        contents='apple juice',
                        amount=10,
                        is_closed=True)
        bottle.put()
        
        tuba = MusicalInstrument(name='tuba',
                                 location=here,
                                 weight=200)
        tuba.put()
        
        # ...
        
        here = db.get(location_key)
        self.response.write('<p>Your location: %s</p>' % here.name)
        
        q = CarryableObject.all()
        q.filter('location', here)
        q.filter('weight >', 100)
        self.response.write('<p>You see the following heavy objects:</p><ul>')
        for obj in q:
            self.response.write('<li>%s</li>' % obj.name)
        self.response.write('</ul>')
        
        db.delete([here, bottle, tuba])
        self.response.write('<p>Entities deleted.</p>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
