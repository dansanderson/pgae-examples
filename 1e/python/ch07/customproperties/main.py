from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class PlayerName(object):
    def __init__(self, first_name, surname):
        self.first_name = first_name
        self.surname = surname

    def is_valid(self):
        return (isinstance(self.first_name, basestring)
                and isinstance(self.surname, basestring)
                and len(self.surname) >= 6)

class PlayerNameProperty(db.Property):
    data_type = basestring

    def __init__(self, verbose_name=None,
                 require_first_name=False, **kwds):
        super(PlayerNameProperty, self).__init__(verbose_name, **kwds)
        self.require_first_name = require_first_name

    def validate(self, value):
        value = super(PlayerNameProperty, self).validate(value)
        if value is not None:
            if not isinstance(value, PlayerName):
                raise db.BadValueError('Property %s must be a PlayerName.' %
                                       self.name)

            # Let the data class have a say in validity.
            if not value.is_valid():
                raise db.BadValueError('Property %s must be a valid PlayerName.' %
                                       self.name)

            # Disallow the serialization delimiter in the first field.
            if value.surname.find('|') != -1:
                raise db.BadValueError(('PlayerName surname in property %s cannot ' +
                                        'contain a "|".') % self.name)

            # Require a first name only if the property declaration asks for it.
            if self.require_first_name and not value.first_name:
                raise db.BadValueError('Property %s PlayerName needs a first_name.'
                                       % self.name)

        return value

    def get_value_for_datastore(self, model_instance):
        # Convert the data object's PlayerName to a unicode.
        return (getattr(model_instance, self.name).surname + u'|'
                + getattr(model_instance, self.name).first_name)

    def make_value_for_datastore(self, value):
        # Convert a unicode to a PlayerName.
        i = value.find(u'|')
        return PlayerName(first_name=value[i+1:],
                          surname=value[:i])

    def default_value(self):
        default = super(PlayerNameProperty, self).default_value()
        if default is not None:
            return default

        return PlayerName('', 'Anonymous')


class Player(db.Model):
    player_name = PlayerNameProperty()

p = Player()
p.player_name = PlayerName('Ned', 'Nederlander')
print '''<p>I can assign PlayerName('Ned', 'Nederlander') to player_name.</p>'''

try:
    p.player_name = PlayerName('Ned', 'Neder|lander')
except db.BadValueError, e:
    print '''<p>I cannot assign PlayerName('Ned', 'Neder|lander') to player_name
because the surname contains a delimiter character.</p>'''

try:
    p.player_name = PlayerName('Ned', 'Neder')
except db.BadValueError, e:
    print '''<p>I cannot assign PlayerName('Ned', 'Neder') to player_name
because it is not considered valid by the PlayerName is_valid() method.
The surname must be longer than 6 characters.</p>'''

p2 = Player()
print ('<p>The default value for a PlayerNameProperty is: %s</p>'
       % (p2.player_name.first_name + ' ' + p2.player_name.surname))


class Player2(db.Model):
    player_name = PlayerNameProperty(require_first_name=True)

p3 = Player(player_name=PlayerName('Ned', 'Nederlander'))

try:
    p3.player_name = PlayerName('', 'Charo')
except db.BadValueError, e:
    print '''<p>I cannot assign PlayerName('', 'Charo') to player_name when
declared as PlayerNameProperty(require_first_name=True).</p>'''

try:
    p4 = Player2()
except db.BadValueError, e:
    print '''<p>I cannot use the default for PlayerNameProperty when
require_first_name=True, because the default value does not have a
first name.</p>'''


print '<p>The time is: %s</p>' % str(datetime.datetime.now())
