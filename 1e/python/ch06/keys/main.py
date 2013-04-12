from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

class MessageBoard(db.Expando):
    pass

class Message(db.Expando):
    pass

def printable_path(k):
    parts = []
    while True:
        parts.insert(0, k.kind() + ':' + str(k.id_or_name()))
        if k.parent() is None:
            break
        else:
            k = k.parent()
    return ' / '.join(parts)

# Creating a new entity group with a root entity:
board = MessageBoard(key_name='The_Archonville_Times')
board.title = 'The Archonville Times'
board.put()

print '<p>board key: %s</p>' % printable_path(board.key())

# Using the object for the "parent" argument:
msg1 = Message(parent=board, key_name='first!')
msg1.put()

print '<p>msg1 key: %s</p>' % printable_path(msg1.key())

# Using a Key for the "parent" argument:
p_key = board.key()
msg2 = Message(parent=p_key, key_name='pk_fest_aug_21')
msg2.put()

print '<p>msg2 key: %s</p>' % printable_path(msg2.key())

# Using an entity that isn't the root as the parent:
msg3 = Message(parent=msg1, key_name='keep_clean')
msg3.put()

print '<p>msg3 key: %s</p>' % printable_path(msg3.key())

# Deriving a key using the ancestor path:
k = db.Key.from_path('MessageBoard', 'The_Archonville_Times',
                     'Message', 'first!',
                     'Message', 'keep_clean')

print '<p>k: %s</p>' % printable_path(k)

# Using a non-existent path part as a parent:
root = db.Key.from_path('MessageBoard', 'The_Baskinville_Post')

msg4 = Message(parent=root)
msg4.put()

print '<p>msg4 key: %s</p>' % printable_path(msg4.key())

msg5 = Message(parent=root)
msg5.put()

print '<p>msg5 key: %s</p>' % printable_path(msg5.key())

db.delete([msg1, msg2, msg3, msg4, msg5, board])
print '<p>Entities deleted.</p>'


print '<p>The time is: %s</p>' % str(datetime.datetime.now())
