package xmpp;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Properties;
import java.util.SimpleTimeZone;
import java.util.logging.Logger;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.EntityNotFoundException;
import com.google.appengine.api.datastore.FetchOptions;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Transaction;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import com.google.appengine.api.utils.SystemProperty;
import com.google.appengine.api.xmpp.JID;
import com.google.appengine.api.xmpp.PresenceShow;
import com.google.apphosting.api.ApiProxy;


@SuppressWarnings("serial")
public class MainPageServlet extends HttpServlet {

    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    /* Presence show values are represented in the Java API as the
     * enum com.google.appengine.api.xmpp.PresenceShow. This app needs
     * to render these values as string names, and also store them in
     * the datastore as a primitive datastore type.  For simplicity,
     * we store these values in the datastore as strings as well.
     * This array is in ordinal order for the enum.
     */
    public static final String[] presenceShowStrings = {
        "none", "away", "chat", "dnd", "xa"
    };


    /* All actions report a message to the admin UI in
     * MainPageServlet.  This message is stored in memcache.  Ideally,
     * we'd use a session ID, so multiple admins can use this
     * simultaneously.  This version only supports one simultaneous
     * admin user.
     */
    private static final String _ADMIN_MESSAGE_KEY = "admin_message";

    public static void setAdminMessage(String message) {
        MemcacheService memcache = MemcacheServiceFactory.getMemcacheService();
        memcache.put(_ADMIN_MESSAGE_KEY, message);
    }

    public static String getAndResetAdminMessage() {
        MemcacheService memcache = MemcacheServiceFactory.getMemcacheService();
        String message = (String) memcache.get(_ADMIN_MESSAGE_KEY);
        memcache.delete(_ADMIN_MESSAGE_KEY);
        return message;
    }


    /* Application status information is stored in the datastore, in a
     * singleton entity.
     */
    private static final Key _SERVICE_STATUS_KEY =
        KeyFactory.createKey("ServiceStatus", "1");

    public static Entity getStatusEntity() {
        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        Transaction txn = datastore.beginTransaction();
        Entity status;
        try {
            status = datastore.get(txn, _SERVICE_STATUS_KEY);
        } catch (EntityNotFoundException e) {
            status = new Entity(_SERVICE_STATUS_KEY);
            status.setProperty("presence_available", true);
            status.setProperty("presence_show",
                               presenceShowStrings[PresenceShow.CHAT.ordinal()]);
            datastore.put(txn, status);
        }
        txn.commit();
        return status;
    }


    // Get or create a user entity for a JID.  This truncates the
    // resource portion of the JID, so multiple user clients are
    // consolidated into one record per account.
    public static Entity getUserEntity(JID jid) {
        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        Transaction txn = datastore.beginTransaction();
        String jidStr = jid.getId();
        if (jidStr.indexOf("/") != -1) {
            jidStr = jidStr.substring(0, jidStr.indexOf("/"));
        }
        Key userKey = KeyFactory.createKey("ChatUser", jidStr);
        Entity userEntity;
        try {
            userEntity = datastore.get(txn, userKey);
        } catch (EntityNotFoundException e) {
            userEntity = new Entity(userKey);
            userEntity.setProperty("jid", jidStr);
            userEntity.setProperty("accepted_invitation", false);
            userEntity.setProperty("is_subscribed", false);
            userEntity.setProperty("is_available", false);
            userEntity.setProperty("presence_show", "chat");
            userEntity.setProperty("status_message", "");
            userEntity.setProperty("last_chat_message", "");
            datastore.put(txn, userEntity);
        }
        txn.commit();
        return userEntity;
    }




    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException, ServletException { 

        String adminMessage = getAndResetAdminMessage();
        req.setAttribute("adminMessage", adminMessage);

        String appId = SystemProperty.applicationId.get();
        String versionId = SystemProperty.applicationVersion.get();
        if (versionId.indexOf(".") != -1) {
            versionId = versionId.substring(0, versionId.indexOf("."));
        }
        String appXmppAddress = "something@" + versionId + ".latest." +
            appId + ".appspotchat.com";
        req.setAttribute("appId", appId);
        req.setAttribute("appXmppAddress", appXmppAddress);

        UserService userService = UserServiceFactory.getUserService();
        User user = userService.getCurrentUser();
        req.setAttribute("user", user);
        req.setAttribute("signoutUrl", userService.createLogoutURL("/"));
        req.setAttribute("isUserAdmin", userService.isUserAdmin());

        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        Query q = new Query("ChatUser").addSort("jid");
        PreparedQuery pq = datastore.prepare(q);
        List<Entity> results = pq.asList(FetchOptions.Builder.withLimit(100));
        req.setAttribute("chatUsers", results);
        req.setAttribute("hasChatUsers", !results.isEmpty());

        req.setAttribute("status", getStatusEntity());

        req.setAttribute("isDevelopment", SystemProperty.environment.value() ==
                         SystemProperty.Environment.Value.Development);
        
        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        req.setAttribute("currentTime", fmt.format(new Date()));

        resp.setContentType("text/html");
        RequestDispatcher jsp = req.getRequestDispatcher("/WEB-INF/home.jsp");
        jsp.forward(req, resp);
    }
}
