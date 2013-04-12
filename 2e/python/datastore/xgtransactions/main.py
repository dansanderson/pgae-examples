# This example demonstrates cross-group (xg) transactions.  This
# feature is only available on the High Replication datastore.  As of
# version 1.7.4, you must start the development server with the
# --high_replication argument to enable this feature.
#
#   dev_appserver.py --high_replication xgtransactions

from google.appengine.ext import db
import datetime
import webapp2

class MessageBoard(db.Expando):
    pass

class Message(db.Expando):
    pass

@db.transactional(xg=True)
def create_message(board_name, message_title, message_text):
    board = db.get(db.Key.from_path('MessageBoard', board_name))
    if not board:
        board = MessageBoard(key_name=board_name)
        board.count = 0

    # Because this is a cross-group (xg) transaction, the Message
    # entity does not need to be in the same entity group as the
    # MessageBoard, and therefore does not need to be in the same
    # entity group as other Messages on the board.
    message = Message()
    message.title = message_title
    message.text = message_text
    message.post_date = datetime.datetime.now()

    # Since the Message is not a child entity of the MessageBoard, we
    # need a way to determine the board that goes with the message,
    # and vice versa.  Store the MessageBoard key.
    message.message_board = board.key()

    board.count += 1

    # Storing the board.count on the Message gives us a monotonically
    # increasing identifier for messages on a board.
    message.message_board_count = board.count

    db.put([board, message])


class MainPage(webapp2.RequestHandler):
    def get(self):

        # The main routine
        for e in db.Query(Message):
            self.response.write(
                '<p>Found message, key: %s  message_board_count: %d</p>'
                % (e.key(), e.message_board_count))

        self.response.write('<form action="/" method="post"><input type="submit" value="Create Messages" /></form>')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))

    def post(self):
        try:
            create_message(
                board_name='The_Archonville_Times',
                message_title='New Character Class Announced: Salesperson',
                message_text='GneroCom has announced that a new ' +
                'character class, salesperson, will be available ' +
                'starting in June...')
            create_message(
                board_name='Betazone',
                message_title='Beta Server Planned Outage',
                message_text='We will be taking the Beta Server down for ' +
                'a software upgrade on Friday evening...')
            create_message(
                board_name='The_Archonville_Times',
                message_title='Name the New Area, Win Prizes!',
                message_text='We\'re so excited about the upcoming launch of '
                'the new game area, we can\'t think of what to call it. Give '
                'us your best name, and you could win a new battleaxe! ...')

            self.response.write('<p>Created 3 new messages.</p>')
        
        except db.TransactionFailedError, e:
            self.response.write('<p>Could not create a new message.</p>')
        
        self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
