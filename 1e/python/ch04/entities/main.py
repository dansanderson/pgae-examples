from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Entity(db.Expando):
    pass


# Creating an entity with a system ID
e1 = Entity()
e1.prop = 1
e1.put()

k1 = e1.key()
print '<p>Entity e1 has a system ID = %d</p>' % k1.id()


# Creating an entity with a key name
e2 = Entity(key_name='alphabeta')
e2.prop = 2
e2.put()

k2 = e2.key()
print '<p>Entity e2 has a key name = %s</p>' % k2.name()


# Getting an entity by a known key
k = db.Key.from_path('Entity', 'alphabeta')
result = db.get(k)

# You could also use this shortcut:
# result = Entity.get_by_key_name('alphabeta')

if result:
    print '<p>Got an entity by key name, prop = %d</p>' % result.prop
else:
    print '<p>Could not find an entity with key name "alphabeta"</p>'


# Inspecting entity objects

e3 = Entity()
assert(not e3.is_saved())

e3.put()
assert(e3.is_saved())

assert(not hasattr(e3, 'prop'))

e3.prop = 3
assert(hasattr(e3, 'prop'))

for n in range(1, 10):
    value = n * n
    setattr(e3, 'prop' + str(n), value)

assert(getattr(e3, 'prop' + str(7)) == 49)

print '<p>Properties of e3:</p><ul>'
for name in e3.instance_properties():
    value = getattr(e3, name)
    print '<li>%s = %d</li>' % (name, value)
print '</ul>'


# Batch put
e4 = Entity()
e5 = Entity()
db.put([e4, e5])


# Delete an entity using the model object
db.delete(e1)

e2.delete()

# Delete by key
k = db.Key.from_path('Entity', 'alphabeta')
db.delete(k)

# Batch delete
db.delete([e4, e5])

print '<p>Entities deleted.</p>'


print '<p>The time is: %s</p>' % str(datetime.datetime.now())
