package xmpp;

import java.io.IOException;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.xmpp.JID;
import com.google.appengine.api.xmpp.Message;
import com.google.appengine.api.xmpp.MessageBuilder;
import com.google.appengine.api.xmpp.XMPPService;
import com.google.appengine.api.xmpp.XMPPServiceFactory;


@SuppressWarnings("serial")
public class ChatServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp)
        throws IOException, ServletException { 

        log.info("ChatServlet");

        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        XMPPService xmpp = XMPPServiceFactory.getXMPPService();

        Message message = xmpp.parseMessage(req);
        JID userJID = message.getFromJid();
        Entity userEntity = MainPageServlet.getUserEntity(userJID);
        userEntity.setProperty("last_chat_message", message.getBody());
        datastore.put(userEntity);

        Message reply = new MessageBuilder()
            .withRecipientJids(userJID)
            .withBody("I got your message! It had " +
                      message.getBody().length() + " characters.")
            .build();
        // (Ignore the send response.)
        xmpp.sendMessage(reply);
    }
}
