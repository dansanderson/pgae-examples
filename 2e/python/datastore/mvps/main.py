from google.appengine.ext import db
import datetime
import webapp2

class Player(db.Expando):
    pass

class Entity(db.Expando):
    def set_prop(self, handler, value):
        '''Sets a property and prints what it is doing.'''
        handler.response.write('<p>%s.prop = %s</p>' % (self.name, repr(value)))
        self.prop = value
        
def show_entity_query(handler, gql):
    '''Prints a GQL query, executes the query and prints results.'''
    handler.response.write('<p>Entity.gql(%s): ' % (repr(gql)))
    for r in Entity.gql(gql):
        handler.response.write(r.name)
    handler.response.write('</p>')

class MainPage(webapp2.RequestHandler):
    def get(self):

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
            self.response.write('<p>Player with "Lava Polo Champion" trophy: '
                                '%s</p>' % p.name)
        
        e1 = Entity(name='e1')
        e1.set_prop(self, [ 3.14, 'a', 'b' ])
        e1.put()
        
        e2 = Entity(name='e2')
        e2.set_prop(self, [ 'a', 1, 6 ])
        e2.put()
        
        show_entity_query(self, "WHERE prop = 3.14")
        show_entity_query(self, "WHERE prop = 6")
        show_entity_query(self, "WHERE prop = 'a'")
        show_entity_query(self, "WHERE prop = 'a' AND prop = 'b'")
        
        e1.set_prop(self, [ 1, 3, 5 ])
        e1.put()
        e2.set_prop(self, [ 4, 6, 8 ])
        e2.put()
        
        show_entity_query(self, "WHERE prop < 2")
        show_entity_query(self, "WHERE prop > 7")
        show_entity_query(self, "WHERE prop > 3")
        
        e2.set_prop(self, [ 2, 3, 4 ])
        e2.put()
        
        show_entity_query(self, "ORDER BY prop ASC")
        show_entity_query(self, "ORDER BY prop DESC")
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
