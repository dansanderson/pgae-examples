from google.appengine.ext import db
import datetime
import webapp2

class Entity(db.Expando):
    pass


class MainPage(webapp2.RequestHandler):
    def get(self):
        # Creating an entity with a system ID
        e1 = Entity()
        e1.prop = 1
        e1.put()
        
        k1 = e1.key()
        self.response.write('<p>Entity e1 has a system ID = %d</p>' % k1.id())
        
        
        # Creating an entity with a key name
        e2 = Entity(key_name='alphabeta')
        e2.prop = 2
        e2.put()
        
        k2 = e2.key()
        self.response.write('<p>Entity e2 has a key name = %s</p>' % k2.name())
        
        
        # Getting an entity by a known key
        k = db.Key.from_path('Entity', 'alphabeta')
        result = db.get(k)
        
        # You could also use this shortcut:
        # result = Entity.get_by_key_name('alphabeta')
        
        if result:
            self.response.write('<p>Got an entity by key name, prop = %d</p>'
                                % result.prop)
        else:
            self.response.write('<p>Could not find an entity with key name '
                                '"alphabeta"</p>')
        
        
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
        
        self.response.write('<p>Properties of e3:</p><ul>')
        for name in e3.instance_properties():
            value = getattr(e3, name)
            self.response.write('<li>%s = %d</li>' % (name, value))
        self.response.write('</ul>')
        
        
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
        
        self.response.write('<p>Entities deleted.</p>')
        
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
