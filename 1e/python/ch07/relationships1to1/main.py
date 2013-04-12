from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class PlayerAvatarImage(db.Model):
    image_data = db.BlobProperty()
    mime_type = db.StringProperty()

class Player(db.Model):
    name = db.StringProperty()
    avatar = db.ReferenceProperty(PlayerAvatarImage)

pai = PlayerAvatarImage()
pai.put()
p = Player(name='druidjane', avatar=pai)
p.put()

player_key = p.key()

# ...

# Feth the name of the player (a string) and a reference to the avatar
# image (a key).
p = db.get(player_key)

print '<p>The Player %s has been fetched from the datastore.' % p.name
print 'Its corresponding PlayerAvatarImage has not yet been fetched.</p>'

# Fetch the avatar image entity and access its image_data property.
image_data = p.avatar.image_data

print '<p>The PlayerAvatarImage has now been fetched.</p>'

db.delete([p, pai])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
