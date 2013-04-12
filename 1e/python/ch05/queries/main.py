from google.appengine.ext import db
import datetime

# Import the stats module because we perform a kind-less query in this
# example, and the datastore stores statistics in entities which are
# returned by such a query.  The Python API requires that the
# corresponding model classes for all entities returned be defined.
# The stats model classes are defined in this module.
from google.appengine.ext.db import stats

print 'Content-Type: text/html'
print ''

class Player(db.Expando):
    pass

player1 = Player(name='wizard612',
                 level=1,
                 score=32,
                 charclass='mage',
                 create_date=datetime.datetime.now())
player1.put()

player2 = Player(name='druidjane',
                 level=10,
                 score=896,
                 charclass='druid',
                 create_date=datetime.datetime.now())
player2.put()

player3 = Player(name='TheHulk',
                 level=7,
                 score=500,
                 charclass='warrior',
                 create_date=datetime.datetime.now())
player3.put()

# Create a Query object using the Query constructor.
q = db.Query(Player)

# Create a Query object using the model class method.
# In both cases, the Query object begins representing a query for all
# entities of the kind 'Player'.
q = Player.all()

# Apply filters to the Query object.
# Results have a 'level' property whose value is greater than 5 and
# less than 20.
q.filter('level >', 5)
q.filter('level <', 20)

# Apply a sort order to the Query object.
# Results are sorted by level, ascending, then by score, descending
# ('-').
q.order('level')
q.order('-score')

# Execute the query and fetch 10 results.
results = q.fetch(10)
print '<p>Executing the query with fetch()...</p>'
for e in results:
    print ('<p>Found result: name=%s, level=%d, score=%d</p>'
           % (e.name, e.level, e.score))

# Execute the query and iterate over all results.
print '<p>Executing the query with iteration...</p>'
for e in q:
    print ('<p>Found result: name=%s, level=%d, score=%d</p>'
           % (e.name, e.level, e.score))

# Build a query with chaining calls.
q2 = Player.all().filter('name =', 'druidjane')

# Get only the first result.
e = q2.get()
if e:
    print ('<p>Using get() to get a result: name=%s, level=%d, score=%d'
           % (e.name, e.level, e.score))
else:
    print '<p>Used get() to get a result, but found none</p>'

# A keys-only query.
q3 = db.Query(Player, keys_only=True)
print '<p>Executing a keys-only query...</p>'
for result_key in q3:
    print '<p>Found result key: %s</p>' % result_key

# Create an object of another kind.
class GameObject(db.Expando):
    pass
gameobj = GameObject().put()

# A kindless query.
#
# Returns all Player and GameObject entities--and anything else in the
# app's datastore.  Note that if you have entities in the datastore of
# kinds other than Player or GameObject, you'll get a "No
# implementation for kind..." error.  You can get this example working
# by creating Expando classes for the other kinds:
#
# class KindName(db.Expando):
#     pass
q4 = db.Query()
print '<p>Executing a kindless query...</p>'
for e in q4:
    print '<p>Found result: key=%s</p>' % e.key()

# Delete all entities.
db.delete([player1, player2, player3, gameobj])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
