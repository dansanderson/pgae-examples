import datetime
import jinja2
import logging
import os
import webapp2
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext.webapp import mail_handlers

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()))

def send_registration_key(sender_addr, user_addr, software_key_data):
    # Use Jinja2 templates to produce the text of the email, in both
    # plaintext and HTML forms.
    message_body_txt_tmpl = template_env.get_template('reg_email.txt')
    message_body_html_tmpl = template_env.get_template('reg_email.html')
    context = {
        'current_user_addr': user_addr,
        'app_email_address': sender_addr,
    }
    message_body_txt = message_body_txt_tmpl.render(context)
    message_body_html = message_body_html_tmpl.render(context)

    message = mail.EmailMessage(
        sender='The Example Team <' + sender_addr + '>',
        to=user_addr,
        subject='Your Example Registration Key',
        body=message_body_txt,
        html=message_body_html,
        attachments=[('example_key.txt', software_key_data)])

    message.send()

class MainPage(webapp2.RequestHandler):
    def get(self):
        app_id = os.environ['APPLICATION_ID']
        if app_id.startswith('s~'):
            app_id = app_id[2:]
        app_email_address = 'support@' + app_id + '.appspotmail.com'
        is_dev_server = os.environ['SERVER_SOFTWARE'].startswith('Development')
        current_time = datetime.datetime.now()
        # app.yaml declares login: required, so this always works:
        current_user_email = users.get_current_user().email()

        send_registration_key(app_email_address,
                              current_user_email,
                              'REGKEY-12345')

        template = template_env.get_template('home.html')
        context = {
            'app_email_address': app_email_address,
            'current_time': current_time,
            'current_user_email': current_user_email,
            'is_dev_server': is_dev_server
        }
        self.response.out.write(template.render(context))

class IncomingMailHandler(mail_handlers.InboundMailHandler):
    def receive(self, message):
        (encoding, payload) = list(message.bodies(content_type='text/plain'))[0]
        body_text = payload.decode()
        logging.info('Received email message from %s, subject "%s": %s' %
                     (message.sender, message.subject, body_text))

application = webapp2.WSGIApplication([IncomingMailHandler.mapping(),
                                       ('/', MainPage)],
                                      debug=True)
