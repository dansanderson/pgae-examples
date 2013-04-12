package xmpp;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.FetchOptions;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import com.google.appengine.api.xmpp.JID;
import com.google.appengine.api.xmpp.Message;
import com.google.appengine.api.xmpp.MessageBuilder;
import com.google.appengine.api.xmpp.MessageType;
import com.google.appengine.api.xmpp.PresenceShow;
import com.google.appengine.api.xmpp.PresenceType;
import com.google.appengine.api.xmpp.SendResponse;
import com.google.appengine.api.xmpp.XMPPService;
import com.google.appengine.api.xmpp.XMPPServiceFactory;


@SuppressWarnings("serial")
public class UpdateServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp)
        throws IOException, ServletException { 

        UserService users = UserServiceFactory.getUserService();
        if (!users.isUserAdmin()) {
            log.info("Non-admin user " + users.getCurrentUser().getEmail() +
                     " attempted to access form handler");
            resp.sendError(404);
            return;
        }

        String jidStr = req.getParameter("jid");
        JID jid = null;
        if (jidStr == null || jidStr.equals("")) {
            jidStr = req.getParameter("jid_other");
        }
        if (jidStr != null) {
            jidStr = jidStr.trim();
            jid = new JID(jidStr);
        }
        String command = req.getParameter("command");

        String adminMessage;

        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        XMPPService xmpp = XMPPServiceFactory.getXMPPService();

        if (jid != null && command.equals("chat")) {
            Message message = new MessageBuilder()
                .withMessageType(MessageType.CHAT)
                .withRecipientJids(jid)
                .withBody(req.getParameter("chat_message"))
                .build();
            SendResponse sendResponse = xmpp.sendMessage(message);
            if (sendResponse.getStatusMap().get(jid) == SendResponse.Status.SUCCESS) {
                adminMessage = "Chat message sent to JID " + jidStr + ".";
            } else if (sendResponse.getStatusMap().get(jid) == SendResponse.Status.INVALID_ID) {
                adminMessage = "Message not sent: invalid JID " + jidStr + ".";
            } else { 
                adminMessage = "Message not sent to " + jidStr + ": internal service error.";
            }
            
        } else if (jid != null && command.equals("invite")) {
            xmpp.sendInvitation(jid);
            adminMessage = "Chat message sent to JID " + jidStr + ".";

        } else if (jid != null && command.equals("probe")) {
            xmpp.sendPresence(jid, PresenceType.PROBE, null, null);
            adminMessage = "A presence probe has been sent to JID " + jidStr + ".";

        } else if (command.equals("presence")) {
            // Store the app's presence.
            Entity statusEntity = MainPageServlet.getStatusEntity();

            if (req.getParameter("presence_available").equals("true")) {
                statusEntity.setProperty("presence_available", true);
            } else if (req.getParameter("presence_available").equals("false")) {
                statusEntity.setProperty("presence_available", false);
            }

            if (req.getParameter("presence_show").equals("chat") ||
                req.getParameter("presence_show").equals("away") ||
                req.getParameter("presence_show").equals("dnd") ||
                req.getParameter("presence_show").equals("xa")) {
                statusEntity.setProperty("presence_show",
                                         req.getParameter("presence_show"));
            }

            statusEntity.setProperty("status_message",
                                     req.getParameter("status_message"));

            datastore.put(statusEntity);

            // Send presence messages to all subscribed users.  As
            // written, this could be slow or broken for a large number
            // of users.  A more robust solution would use a task queue
            // and a query cursor.  (Unlike sendMessage(),
            // sendPresence() only accepts one JID at a time.)
            Query q = new Query("ChatUser").addFilter("is_subscribed",
                                                      Query.FilterOperator.EQUAL,
                                                      true);
            PreparedQuery pq = datastore.prepare(q);
            for (Entity e : pq.asIterable()) {
                String recipJidStr = (String)(e.getProperty("jid"));
                JID recipJid = new JID(recipJidStr);
                xmpp.sendPresence(recipJid,
                                  ((Boolean)statusEntity.getProperty("presence_available")) ?
                                  PresenceType.AVAILABLE : PresenceType.UNAVAILABLE,
                                  PresenceShow.valueOf(((String)statusEntity.getProperty("presence_show")).toUpperCase()),
                                  (String)statusEntity.getProperty("status_message"));
            }

            adminMessage = "The app is now " +
                ((Boolean)statusEntity.getProperty("presence_available") ? "" : "un") +
                "available and \"" + statusEntity.getProperty("presence_show") +
                "\" with message \"" + statusEntity.getProperty("status_message") +
                "\", and all subscribed users have been informed.";

        } else if (command.equals("clear_users")) { 
            // This actually deletes only 1,000 users.  A scalable
            // solution would use task queues and query cursors to
            // iterate over and delete all entities.
            Query q = new Query("ChatUser").setKeysOnly();
            PreparedQuery pq = datastore.prepare(q);
            List<Entity> entityList = pq.asList(FetchOptions.Builder.withLimit(1000));
            List<Key> keyList = new ArrayList();
            for (Entity e : entityList) {
                keyList.add(e.getKey());
            }
            datastore.delete(keyList);

            adminMessage = "All user records have been deleted.";

        } else {
            adminMessage = "The submitted form was invalid.";
        }

        MainPageServlet.setAdminMessage(adminMessage);
        resp.sendRedirect("/");
    }
}
