from google.appengine.ext import db
from google.appengine.ext.db import polymodel
import datetime

print 'Content-Type: text/html'
print ''

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
    def play(self):
        print '<p>You play the %s.  Everyone is impressed!</p>' % self.name

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
print '<p>Your location: %s</p>' % here.name

q = CarryableObject.all()
q.filter('location', here)
q.filter('weight >', 100)
print '<p>You see the following heavy objects:</p><ul>'
for obj in q:
    print '<li>%s</li>' % obj.name
print '</ul>'

db.delete([here, bottle, tuba])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
