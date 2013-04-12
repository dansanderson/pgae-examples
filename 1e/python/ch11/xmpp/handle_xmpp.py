import re
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def do_arithmetic(question):
    m = re.match(r'\s*(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)', question)
    if not m:
        return None
    (first, op, second) = m.groups()
    first = float(first)
    second = float(second)
    if op == '+':
        answer = first + second
    elif op == '-':
        answer = first - second
    elif op == '*':
        answer = first * second
    else:
        # op == '/'
        if second == 0:
            answer = 'Inf'
        else:
            answer = first / second
    return str(answer)

class IncomingXMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)

        answer = do_arithmetic(message.body)
        if answer is None:
            message.reply('I didn\'t understand: ' + message.body)
        else:
            message.reply('The answer is: ' + answer)

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/',
                                       IncomingXMPPHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
