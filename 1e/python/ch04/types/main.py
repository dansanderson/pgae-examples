from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Entity(db.Expando):
    pass

e1 = Entity()
e1.string_prop = 'string value, limited to 500 bytes'
e1.text_prop = db.Text('text value, can be up to 1 megabyte')
e1.short_blob_prop = db.ByteString('\x6B\x74\x68\x78\x62\x79\x65')
e1.blob_prop = db.Blob('\x6B\x74\x68\x78\x62\x79\x65')
e1.boolean_prop = True
e1.integer_prop = 99
e1.float_prop = 3.14159
e1.datetime_prop = datetime.datetime.now()
e1.null_prop = None
e1.geopt_prop = db.GeoPt(47.620339, -122.349629)

e1.multivalued_prop = ['string value', True, 3.14159]

db.put(e1)
print '<p>Created an entity, key: %s</p>' % e1.key()

e2 = Entity()
e2.key_prop = e1.key()
db.put(e2)
print '<p>Created an entity, key: %s</p>' % e2.key()

a = Entity()
a.prop1 = 'abc'
a.prop2 = None
a.put()
# a has two properties: prop1 and prop2.  prop2 has a null value.

b = Entity()
b.prop1 = 'def'
b.put()
# b has one property: prop1.  It does not have a property named prop2.

b.prop2 = 123
b.put()
# b now has a property named prop2.

del b.prop2
b.put()
# b no longer has a property named prop2.

db.delete([e1, e2, a, b])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
