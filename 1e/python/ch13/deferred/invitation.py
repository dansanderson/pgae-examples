from google.appengine.api import mail
import logging

_INVITATION_MESSAGE_BODY = '''
You have been invited to join our community...
'''

def send_invitation(recipient):
    mail.send_mail('support@example.com',
                   recipient,
                   'You\'re invited!',
                   _INVITATION_MESSAGE_BODY)
    logging.info('Sent invitation to %s' % recipient)
