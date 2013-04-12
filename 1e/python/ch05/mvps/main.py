from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Player(db.Expando):
    pass

p1 = Player(name='druidjane')
p1.trophies = ['Lava Polo Champion',
              'World Building 2008, Bronze',
              'Glarcon Fighter, 2nd class']
p1.put()

p2 = Player(name='wizard612')
p2.trophies = ['Glarcon Fighter, 3rd class',
               'Lava Polo Champion']
p2.put()

p3 = Player(name='TheHulk')
p3.trophies = ['World Building 2008, Silver']
p3.put()

q = Player.gql("WHERE trophies = 'Lava Polo Champion'")
for p in q:
    print '<p>Player with "Lava Polo Champion" trophy: %s</p>' % p.name


class Entity(db.Expando):
    def set_prop(self, value):
        '''Sets a property and prints what it is doing.'''
        print '<p>%s.prop = %s</p>' % (self.name, repr(value))
        self.prop = value
        
def show_entity_query(gql):
    '''Prints a GQL query, executes the query and prints results.'''
    print '<p>Entity.gql(%s): ' % (repr(gql))
    for r in Entity.gql(gql):
        print r.name
    print '</p>'

e1 = Entity(name='e1')
e1.set_prop([ 3.14, 'a', 'b' ])
e1.put()

e2 = Entity(name='e2')
e2.set_prop([ 'a', 1, 6 ])
e2.put()

show_entity_query("WHERE prop = 3.14")
show_entity_query("WHERE prop = 6")
show_entity_query("WHERE prop = 'a'")
show_entity_query("WHERE prop = 'a' AND prop = 'b'")

e1.set_prop([ 1, 3, 5 ])
e1.put()
e2.set_prop([ 4, 6, 8 ])
e2.put()

show_entity_query("WHERE prop < 2")
show_entity_query("WHERE prop > 7")
show_entity_query("WHERE prop > 3")

e2.set_prop([ 2, 3, 4 ])
e2.put()

show_entity_query("ORDER BY prop ASC")
show_entity_query("ORDER BY prop DESC")

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
