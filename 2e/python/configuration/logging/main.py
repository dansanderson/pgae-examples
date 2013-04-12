import datetime
import logging
import sys
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        logging.debug('debug level')
        logging.info('info level')
        logging.warning('warning level')
        logging.error('error level')
        logging.critical('critical level')

        sys.stderr.write('stderr write, logged at the error level\n')

        self.response.write('<p>Messages logged.</p>')
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

