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

# Create a GqlQuery object using the GqlQuery constructor.
q = db.GqlQuery('SELECT * FROM Player ' +
                '        WHERE level > 5 ' +
                '          AND level < 20 ' +
                '     ORDER BY level ASC, score DESC')

# Create a GqlQuery object using the model class method.
q = Player.gql('        WHERE level > 5 ' +
               '          AND level < 20 ' +
               '     ORDER BY level ASC, score DESC')

# Parameter substitution with positional arguments.
q = db.GqlQuery('SELECT * FROM Player ' +
                '        WHERE level > :1 ' +
                '          AND level < :2 ' +
                '     ORDER BY level ASC, score DESC',
                5, 20)

# Parameter substitution with keyword arguments.
q = db.GqlQuery('SELECT * FROM Player ' +
                '        WHERE level > :min_level ' +
                '          AND level < :max_level ' +
                '     ORDER BY level ASC, score DESC',
                min_level=5, max_level=20)

# Parameter substitution with late binding.
q = db.GqlQuery('SELECT * FROM Player ' +
                '        WHERE level > :min_level ' +
                '          AND level < :max_level ' +
                '     ORDER BY level ASC, score DESC')
q.bind(min_level=5, max_level=20)


# Execute the query and iterate over all results.
print '<p>Executing the query with iteration...</p>'
for e in q:
    print ('<p>Found result: name=%s, level=%d, score=%d</p>'
           % (e.name, e.level, e.score))

# An example of a date-time literal in GQL.
q = db.GqlQuery('SELECT * FROM Player ' +
                '        WHERE create_date < DATETIME(2012, 12, 31, 23, 59, 59)')

# A keys-only query with GqlClass.
q2 = db.GqlQuery('SELECT __key__ FROM Player')
print '<p>Executing a keys-only query...</p>'
for result_key in q2:
    print '<p>Found result key: %s</p>' % result_key

# Create an object of another kind.
class GameObject(db.Expando):
    pass
gameobj = GameObject().put()

# A kindless query with GqlClass.
#
# Returns all Player and GameObject entities--and anything else in the
# app's datastore.  Note that if you have entities in the datastore of
# kinds other than Player or GameObject, you'll get a "No
# implementation for kind..." error.  You can get this example working
# by creating Expando classes for the other kinds:
#
# class KindName(db.Expando):
#     pass
q4 = db.GqlQuery('SELECT *')
print '<p>Executing a kindless query...</p>'
for e in q4:
    print '<p>Found result: key=%s</p>' % e.key()

# Delete all entities.
db.delete([player1, player2, player3, gameobj])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
