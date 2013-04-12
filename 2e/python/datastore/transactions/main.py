from google.appengine.ext import db
import datetime
import webapp2

entities_to_delete = []

class MessageBoard(db.Expando):
    pass

class Message(db.Expando):
    pass

@db.transactional
def create_message(board_name, message_name, message_title, message_text):
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


class MainPage(webapp2.RequestHandler):
    def get(self):

        # The main routine
        try:
            create_message(
                board_name='The_Archonville_Times',
                message_name='new_character_class_announced',
                message_title='New Character Class Announced: Salesperson',
                message_text='GneroCom has announced that a new ' +
                'character class, salesperson, will be available ' +
                'starting in June...')
            self.response.write('<p>Created a new message.</p>')
        
        except db.TransactionFailedError, e:
            self.response.write('<p>Could not create a new message.</p>')
        
        for k in db.Query(Message, keys_only=True):
            self.response.write('<p>Found message, key: %s</p>' % k)
        
        db.delete(entities_to_delete)
        self.response.write('<p>Deleted entities.</p>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
