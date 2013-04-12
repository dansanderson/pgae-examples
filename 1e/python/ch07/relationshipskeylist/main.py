from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class Player(db.Model):
    name = db.StringProperty()
    guilds = db.ListProperty(db.Key)

class Guild(db.Model):
    name = db.StringProperty()

    @property
    def members(self):
        return Player.all().filter('guilds', self.key())

# Create some test data.
g1 = Guild(name='The Foo Battlers')
g2 = Guild(name='The Bar Fighters')
db.put([g1, g2])

p1 = Player(name='druidjane', guilds=[g1.key(), g2.key()])
p2 = Player(name='TheHulk', guilds=[g2.key()])
db.put([p1, p2])

player_key = p1.key()
guild_key = g2.key()

# ...

# Guilds to which a player belongs:
p = db.get(player_key)
guilds = db.get(p.guilds)  # batch get using list of keys
print '<p>Guilds to which druidjane belongs:</p><ul>'
for guild in guilds:
    print '<li>%s</li>' % guild.name
print '</ul>'

# Players that belong to a guild:
g = db.get(guild_key)
print '<p>Members of The Bar Fighters:</p><ul>'
for player in g.members:
    print '<li>%s</li>' % player.name
print '</ul>'

db.delete([p1, p2, g1, g2])
print '<p>Entities deleted.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
