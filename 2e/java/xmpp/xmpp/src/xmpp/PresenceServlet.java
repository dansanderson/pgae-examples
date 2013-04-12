package xmpp;

import java.io.IOException;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.xmpp.JID;
import com.google.appengine.api.xmpp.Presence;
import com.google.appengine.api.xmpp.PresenceShow;
import com.google.appengine.api.xmpp.PresenceType;
import com.google.appengine.api.xmpp.XMPPService;
import com.google.appengine.api.xmpp.XMPPServiceFactory;


@SuppressWarnings("serial")
public class PresenceServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp)
        throws IOException, ServletException { 

        log.info("PresenceServlet: ..." + req.getPathInfo());

        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        XMPPService xmpp = XMPPServiceFactory.getXMPPService();

        Presence presence = xmpp.parsePresence(req);
        JID userJID = presence.getFromJid();

        if (presence.getPresenceType() == PresenceType.AVAILABLE ||
            presence.getPresenceType() == PresenceType.UNAVAILABLE) {
            // Store the user's presence.
            Entity userEntity = MainPageServlet.getUserEntity(userJID);
            userEntity.setProperty("is_available",
                                   presence.getPresenceType() == PresenceType.AVAILABLE);

            // Interpret no show value or "none" as "chat".
            if (presence.getPresenceShow() == null ||
                presence.getPresenceShow() == PresenceShow.NONE) {
                userEntity.setProperty("presence_show", "chat");
            } else {
                userEntity.setProperty("presence_show",
                                       presence.getPresenceShow().toString().toLowerCase());
            }

            userEntity.setProperty("status_message", presence.getStatus());
            datastore.put(userEntity);

        } else if (presence.getPresenceType() == PresenceType.PROBE) {
            // Respond to the probe by sending the app's presence.
            Entity statusEntity = MainPageServlet.getStatusEntity();
            xmpp.sendPresence(userJID,
                              ((Boolean)statusEntity.getProperty("presence_available")) ?
                              PresenceType.AVAILABLE : PresenceType.UNAVAILABLE,
                              PresenceShow.valueOf(((String)statusEntity.getProperty("presence_show")).toUpperCase()),
                              (String)statusEntity.getProperty("status_message"));
        }
    }
}
