import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import mail_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

class MyMailHandler(mail_handlers.InboundMailHandler):
    def receive(self, message):
        (encoding, payload) = list(message.bodies(content_type='text/plain'))[0]
        body_text = payload.decode()
        logging.info('Received email message from %s: %s' % (message.sender,
                                                             body_text))

application = webapp.WSGIApplication([MyMailHandler.mapping()],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
