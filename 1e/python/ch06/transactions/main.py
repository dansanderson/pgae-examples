from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

entities_to_delete = []

class MessageBoard(db.Expando):
    pass

class Message(db.Expando):
    pass

def create_message_txn(board_name, message_name, message_title, message_text):
    board = db.get(db.Key.from_path('MessageBoard', board_name))
    if not board:
        board = MessageBoard(key_name=board_name)
        board.count = 0

    message = Message(key_name=message_name, parent=board)
    message.title = message_title
    message.text = message_text
    message.post_date = datetime.datetime.now()

    board.count += 1

    db.put([board, message])
    entities_to_delete.extend([board, message])


# The main routine
try:
    db.run_in_transaction(create_message_txn,
                          board_name='The_Archonville_Times',
                          message_name='new_character_class_announced',
                          message_title='New Character Class Announced: Salesperson',
                          message_text='GneroCom has announced that a new ' +
                          'character class, salesperson, will be available ' +
                          'starting in June...')
    print '<p>Created a new message.</p>'

except db.TransactionFailedError, e:
    print '<p>Could not create a new message.</p>'

for k in db.Query(Message, keys_only=True):
    print '<p>Found message, key: %s</p>' % k

db.delete(entities_to_delete)
print '<p>Deleted entities.</p>'


print '<p>The time is: %s</p>' % str(datetime.datetime.now())
