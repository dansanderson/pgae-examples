import datetime
import jinja2
import logging
import os
import webapp2
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.api import xmpp

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()))

# This uses a cheap method to store messages for the admin UI that only
# allows one simultaneous admin user.  Better would be to make a
# session key for each active admin user.
_ADMIN_MESSAGE_KEY = 'admin_message'

_PRESENCE_SHOW_OPTIONS = [xmpp.PRESENCE_SHOW_AWAY,
                          xmpp.PRESENCE_SHOW_CHAT,
                          xmpp.PRESENCE_SHOW_DND,
                          xmpp.PRESENCE_SHOW_XA]


# This stores the app's current status in a singleton datastore entity.
_SERVICE_STATUS_KEY = '1'

class ServiceStatus(db.Model):
    presence_available = db.BooleanProperty(default=True)
    presence_show = db.StringProperty(
        choices=_PRESENCE_SHOW_OPTIONS,
        default=xmpp.PRESENCE_SHOW_CHAT)
    status_message = db.StringProperty()
    last_error = db.StringProperty()
    last_error_datetime = db.DateTimeProperty()

def get_status_entity():
    return ServiceStatus.get_or_insert(_SERVICE_STATUS_KEY)


def truncate_jid(jid):
    # Remove the "resource" portion of a JID.
    if jid:
        i = jid.find('/')
        if i != -1:
            jid = jid[:i]
    return jid


class ChatUser(db.Model):
    jid = db.StringProperty()
    accepted_invitation = db.BooleanProperty(default=False)
    is_subscribed = db.BooleanProperty(default=False)
    is_available = db.BooleanProperty(default=False)
    presence_show = db.StringProperty(
        choices=_PRESENCE_SHOW_OPTIONS,
        default=xmpp.PRESENCE_SHOW_CHAT)
    status_message = db.StringProperty()
    last_chat_message = db.StringProperty()


class ChatHandler(webapp2.RequestHandler):
    def post(self):
        logging.info('ChatHandler: %r' % self.request.POST)

        message = xmpp.Message(self.request.POST)
        user = ChatUser.get_or_insert(truncate_jid(message.sender))
        user.jid = message.sender
        user.last_chat_message = message.body
        user.put()

        message.reply('I got your message! '
                      'It had %d characters.' % len(message.body))


class SubscriptionHandler(webapp2.RequestHandler):
    def post(self, command):
        logging.info('SubscriptionHandler: %r' % self.request.POST)

        user_jid = truncate_jid(self.request.POST.get('from'))
        user = ChatUser.get_or_insert(user_jid)
        user.jid = user_jid
        if command == 'subscribed':
            user.accepted_invitation = True
        elif command == 'unsubscribed':
            user.accepted_invitation = False
        elif command == 'subscribe':
            user.is_subscribed = True
        elif command == 'unsubscribe':
            user.is_subscribed = False
        user.put()


class PresenceHandler(webapp2.RequestHandler):
    def post(self, command):
        logging.info('PresenceHandler: %r' % self.request.POST)

        user_jid = truncate_jid(self.request.POST.get('from'))

        if command == 'available' or command == 'unavailable':
            # Store the user's presence.
            user = ChatUser.get_or_insert(user_jid)
            user.jid = user_jid
            user.is_available = command == 'available'

            show = self.request.POST.get('show')
            if show and show in _PRESENCE_SHOW_OPTIONS:
                user.presence_show = show
            else:
                # The XMPP standard says an omitted show value is
                # equivalent to chat.
                user.presence_show = xmpp.PRESENCE_SHOW_CHAT

            status_message = self.request.POST.get('status')
            if status_message is not None:
                user.status_message = status_message
            
            user.put()

        elif command == 'probe':
            # Respond to the probe by sending the app's presence.
            status = get_status_entity()
            xmpp.send_presence(
                jid,
                presence_type=(xmpp.PRESENCE_TYPE_UNAVAILABLE
                               if status.presence_available
                               else xmpp.PRESENCE_TYPE_AVAILABLE),
                presence_show=status.presence_show)


class ErrorHandler(webapp2.RequestHandler):
    def post(self):
        logging.info('ErrorHandler: %r' % self.request.POST)

        status = get_status_entity()
        status.last_error = repr(self.request.POST)
        status.last_error_datetime = datetime.datetime.now()
        status.put()


class FormHandler(webapp2.RequestHandler):
    def post(self):
        if not users.is_current_user_admin():
            logging.info("Non-admin user %s attempted to access form handler"
                         % users.get_current_user().email())
            self.error(404)
            return
        
        jid = self.request.POST.get('jid') or self.request.POST.get('jid_other')
        if jid:
            jid = jid.strip()
        command = self.request.POST.get('command')

        if jid and command == 'chat':
            xmpp.send_message(jid, self.request.POST.get('chat_message'))
            msg = 'Chat message sent to JID %s.' % jid

        elif jid and command == 'invite':
            xmpp.send_invite(jid)
            msg = 'JID %s has been invited to chat.' % jid

        elif jid and command == 'probe':
            xmpp.send_presence(jid, presence_type=xmpp.PRESENCE_TYPE_PROBE)
            msg = 'A presence probe has been sent to JID %s.' % jid

        elif command == 'presence':
            # Store the app's presence.
            status = get_status_entity()
            if self.request.POST.get('presence_available') in ('true', 'false'):
                status.presence_available = self.request.POST.get('presence_available') == 'true'
            if self.request.POST.get('presence_show') in _PRESENCE_SHOW_OPTIONS:
                status.presence_show = self.request.POST.get('presence_show')
            status.status_message = self.request.POST.get('status_message')
            status.put()

            # Send presence messages to all subscribed users.  As
            # written, this could be slow or broken for a large number
            # of users.  A more robust solution would use a task queue
            # and a query cursor.  (Unlike send_message(),
            # send_presence() only accepts one JID at a time.)
            for user in ChatUser.all().filter('is_subscribed', True):
                xmpp.send_presence(
                    user.jid,
                    status=status.status_message,
                    presence_type=(xmpp.PRESENCE_TYPE_AVAILABLE
                                   if status.presence_available
                                   else xmpp.PRESENCE_TYPE_UNAVAILABLE),
                    presence_show=status.presence_show)

            msg = ('The app is now %s and "%s" with message "%s", and all subscribed users have been informed.'
                   % ('available' if status.presence_available else 'unavailable',
                      status.presence_show, status.status_message))

        elif command == 'clear_users':
            db.delete(ChatUser.all(keys_only=True))
            msg = 'All user records have been deleted.'
            
        else:
            msg = 'The submitted form was invalid.'

        memcache.set(_ADMIN_MESSAGE_KEY, msg)
        self.redirect('/')


class MainPage(webapp2.RequestHandler):
    def get(self):
        admin_message = memcache.get(_ADMIN_MESSAGE_KEY)
        memcache.delete(_ADMIN_MESSAGE_KEY)

        app_id = os.environ['APPLICATION_ID']
        if app_id.startswith('dev~'):
            app_id = app_id[len('dev~'):]
        version_id = os.environ['CURRENT_VERSION_ID']
        version_id = version_id[:version_id.find('.')]

        app_xmpp_address = ('something@%s.latest.%s.appspotchat.com'
                            % (version_id, app_id))
        current_time = datetime.datetime.now()
        is_dev_server = os.environ['SERVER_SOFTWARE'].startswith('Development')

        chat_users = ChatUser.all().order('jid').fetch(100)
        for user in chat_users:
            # TODO: this is always returning False when on App Engine?
            user._gtalk_presence = xmpp.get_presence(user.jid)

        status = get_status_entity()

        template = template_env.get_template('home.html')
        context = {
            'admin_message': admin_message,
            'app_id': app_id,
            'app_xmpp_address': app_xmpp_address,
            'current_time': current_time,
            'is_dev_server': is_dev_server,

            'has_chat_users': len(chat_users) > 0,
            'chat_users': chat_users,
            'status': status,

            'current_user': users.get_current_user(),
            'is_user_admin': users.is_current_user_admin(),
            'signout_url': users.create_logout_url('/'),
        }
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication(
    [('/_ah/xmpp/message/chat/', ChatHandler),
     ('/_ah/xmpp/subscription/(.*)/', SubscriptionHandler),
     ('/_ah/xmpp/presence/(.*)/', PresenceHandler),
     ('/_ah/xmpp/error/', ErrorHandler),
     ('/update', FormHandler),
     ('/', MainPage)],
    debug=True)
