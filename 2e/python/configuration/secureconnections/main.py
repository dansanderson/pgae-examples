import datetime
import os
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        if os.environ.get('HTTPS') == 'on':
            self.response.write(
                '<p>This page was accessed over a secure connection.</p>')
        else:
            self.response.write(
                '<p>This page was accessed over a normal (non-secure) '
                'connection.</p>')

        server_name = os.environ.get('SERVER_NAME')
        server_port = os.environ.get('SERVER_PORT')
        is_dev_server = os.environ['SERVER_SOFTWARE'].startswith('Development')

        self.response.write('<ul>')
        if is_dev_server:
            for path in ('', 'always', 'never', 'optional'):
                url = 'http://%s:%s/%s' % (server_name, server_port, path)
                self.response.write('<li><a href="' + url + '">' +
                                    url + '</a></li>')
        else:
            for scheme in ('http', 'https'):
                for path in ('', 'always', 'never', 'optional'):
                    url = '%s://%s/%s' % (scheme, server_name, path)
                    self.response.write('<li><a href="' + url + '">' +
                                        url + '</a></li>')
        self.response.write('</ul>')

        if is_dev_server:
            self.response.write('<p>The development server does not '
                                'support HTTPS, only HTTP.</p>')

        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/.*', MainPage)], debug=True)
