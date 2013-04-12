package xmpp;

import java.io.IOException;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.xmpp.JID;
import com.google.appengine.api.xmpp.Subscription;
import com.google.appengine.api.xmpp.SubscriptionType;
import com.google.appengine.api.xmpp.XMPPService;
import com.google.appengine.api.xmpp.XMPPServiceFactory;


@SuppressWarnings("serial")
public class SubscriptionServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    public void doPost(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException, ServletException { 

        log.info("SubscriptionServlet: ..." + req.getPathInfo());

        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        XMPPService xmpp = XMPPServiceFactory.getXMPPService();

        Subscription sub = xmpp.parseSubscription(req);
        JID userJID = sub.getFromJid();
        Entity userEntity = MainPageServlet.getUserEntity(userJID);

        if (sub.getSubscriptionType() == SubscriptionType.SUBSCRIBED) {
            userEntity.setProperty("accepted_invitation", true);
        } else if (sub.getSubscriptionType() == SubscriptionType.UNSUBSCRIBED) {
            userEntity.setProperty("accepted_invitation", false);
        } else if (sub.getSubscriptionType() == SubscriptionType.SUBSCRIBE) {
            userEntity.setProperty("is_subscribed", true);
        } else if (sub.getSubscriptionType() == SubscriptionType.UNSUBSCRIBE) {
            userEntity.setProperty("is_subscribed", false);
        }
        datastore.put(userEntity);
    }
}
