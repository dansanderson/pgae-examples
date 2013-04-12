import datetime
from google.appengine.api import mail
from google.appengine.api import users

# Replace this with the email address of a registered developer of the
# app.
SENDER_ADDRESS = 'admin@example.com'

def send_registration_key(user_addr, software_key_data):
    message_body = '''
    Thank you for purchasing The Example App, the best
    example on the market!  Your registration key is attached
    to this email.

    To install your key, download the attachment, then select
    "Register..." from the Help menu.  Select the key file, then click
    "Register".

    You can download the app at any time from:
      http://www.example.com/downloads/

    [This is not a real website.]

    Thanks again!

    The Example Team
    '''

    html_message_body = '''
    <p>Thank you for purchasing The Example App, the best
    example on the market!  Your registration key is attached
    to this email.</p>

    <p>To install your key, download the attachment, then select
    <b>Register...</b> from the <b>Help</b> menu.  Select the key file, then
    click <b>Register</b>.</p>

    <p>You can download the app at any time from:</p>
    
    <p>
      <a href="http://www.example.com/downloads/">
        http://www.example.com/downloads/
      </a>
    </p>

    <p>[This is not a real website.]</p>

    <p>Thanks again!</p>

    <p>The Example Team<br />
    <img src="http://www.example.com/images/logo_email.gif" /></p>
    '''

    message = mail.EmailMessage(
        sender='The Example Team <' + SENDER_ADDRESS + '>',
        to=user_addr,
        subject='Your Example Registration Key',
        body=message_body,
        html=html_message_body,
        attachments=[('example_key.txt', software_key_data)])

    message.send()


print 'Content-Type: text/html'
print ''

email_addr = users.get_current_user().email()
send_registration_key(email_addr, 'REGKEY-12345')

print '<p>Email sent to %s.</p>' % email_addr

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
