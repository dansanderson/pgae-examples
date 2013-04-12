import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class TaskHandler(webapp.RequestHandler):
    def post(self):
        if self.request.get('firstname', None) is None:
            logging.info('Task ran, no parameters')
        else:
            logging.info('Task ran, address = %s, firstname = %s'
                         % (self.request.get('address'),
                            self.request.get('firstname')))

application = webapp.WSGIApplication([('/.*', TaskHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
