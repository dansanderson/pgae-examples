from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

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

here = Location(name='Upper Shore')
here.put()

bottle = Bottle(name='heavy jug',
                location=here,
                weight=125,
                contents='apple juice',
                amount=10,
                is_closed=True)
bottle.put()
print '<p>Created a Bottle with inherited property declarations.</p>'

db.delete([here, bottle])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
