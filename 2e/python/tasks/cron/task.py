import logging
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        logging.info('Scheduled task ran.')

app = webapp2.WSGIApplication([('/scheduledtask', MainPage)], debug=True)
