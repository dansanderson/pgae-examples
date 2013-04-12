package clock;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

@SuppressWarnings("serial")
public class PrefsServlet extends HttpServlet {
    public void doPost(HttpServletRequest req,
            HttpServletResponse resp)
          throws IOException {
        UserService userService = UserServiceFactory.getUserService();
        User user = userService.getCurrentUser();

        DatastoreService ds = DatastoreServiceFactory.getDatastoreService();
        Key userKey = KeyFactory.createKey("UserPrefs", user.getUserId());
        Entity userPrefs = new Entity(userKey);

        try {
            int tzOffset = new Integer(req.getParameter("tz_offset")).intValue();

            userPrefs.setProperty("tz_offset", tzOffset);
            userPrefs.setProperty("user", user);
            ds.put(userPrefs);

        } catch (NumberFormatException nfe) {
            // User entered a value that wasn't an integer. Ignore for now.
        }

        resp.sendRedirect("/");
    }
}
