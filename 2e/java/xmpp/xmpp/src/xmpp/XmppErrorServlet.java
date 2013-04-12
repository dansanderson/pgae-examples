package xmpp;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Date;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.xmpp.Message;
import com.google.appengine.api.xmpp.XMPPService;
import com.google.appengine.api.xmpp.XMPPServiceFactory;


@SuppressWarnings("serial")
public class XmppErrorServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp)
        throws IOException, ServletException { 

        log.info("XmppErrorServlet");

        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        XMPPService xmpp = XMPPServiceFactory.getXMPPService();

        Message message = xmpp.parseMessage(req);
        Entity statusEntity = MainPageServlet.getStatusEntity();
        statusEntity.setProperty("last_error", message.getBody());
        statusEntity.setProperty("Last_error_datetime", new Date());
        datastore.put(statusEntity);
    }
}
