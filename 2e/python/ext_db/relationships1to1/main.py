from google.appengine.ext import db
import datetime
import webapp2

class PlayerAvatarImage(db.Model):
    image_data = db.BlobProperty()
    mime_type = db.StringProperty()

class Player(db.Model):
    name = db.StringProperty()
    avatar = db.ReferenceProperty(PlayerAvatarImage)

class MainPage(webapp2.RequestHandler):
    def get(self):

        pai = PlayerAvatarImage()
        pai.put()
        p = Player(name='druidjane', avatar=pai)
        p.put()
        
        player_key = p.key()
        
        # ...
        
        # Feth the name of the player (a string) and a reference to the avatar
        # image (a key).
        p = db.get(player_key)
        
        self.response.write(
            '<p>The Player %s has been fetched from the datastore. '
            'Its corresponding PlayerAvatarImage has not yet been fetched.</p>'
            % p.name)
        
        # Fetch the avatar image entity and access its image_data property.
        image_data = p.avatar.image_data
        
        self.response.write(
            '<p>The PlayerAvatarImage has now been fetched.</p>')
        
        db.delete([p, pai])
        self.response.write('<p>Entities deleted.</p>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
