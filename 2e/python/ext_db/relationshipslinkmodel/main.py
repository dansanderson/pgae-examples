from google.appengine.ext import db
import datetime
import webapp2

class Player(db.Model):
    name = db.StringProperty()

class Guild(db.Model):
    name = db.StringProperty()

class GuildMembership(db.Model):
    player = db.ReferenceProperty(Player, collection_name='guild_memberships')
    guild = db.ReferenceProperty(Guild, collection_name='player_memberships')

class MainPage(webapp2.RequestHandler):
    def get(self):

        # Create some test data.
        g1 = Guild(name='The Foo Battlers')
        g2 = Guild(name='The Bar Fighters')
        p1 = Player(name='druidjane')
        p2 = Player(name='TheHulk')
        db.put([p1, p2, g1, g2])
        
        gm1 = GuildMembership(player=p1, guild=g1)
        gm2 = GuildMembership(player=p1, guild=g2)
        gm3 = GuildMembership(player=p2, guild=g2)
        db.put([gm1, gm2, gm3])
        
        player_key = p1.key()
        guild_key = g2.key()
        
        # ...
        
        # Guilds to which a player belongs:
        p = db.get(player_key)
        self.response.write('<p>Guilds to which druidjane belongs:</p><ul>')
        for gm in p.guild_memberships:
            self.response.write('<li>%s</li>' % gm.guild.name)
        self.response.write('</ul>')
        
        # Players that belong to a guild:
        g = db.get(guild_key)
        self.response.write('<p>Members of The Bar Fighters:</p><ul>')
        for gm in g.player_memberships:
            self.response.write('<li>%s</li>' % gm.player.name)
        self.response.write('</ul>')
        
        db.delete([p1, p2, g1, g2, gm1, gm2, gm3])
        self.response.write('<p>Entities deleted.</p>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
