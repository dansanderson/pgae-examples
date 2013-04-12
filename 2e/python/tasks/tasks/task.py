import logging
import webapp2

class TaskHandler(webapp2.RequestHandler):
    def post(self):
        if self.request.get('firstname', None) is None:
            logging.info('Task ran, no parameters')
        else:
            logging.info('Task ran, address = %s, firstname = %s'
                         % (self.request.get('address'),
                            self.request.get('firstname')))

app = webapp2.WSGIApplication([('/.*', TaskHandler)], debug=True)
