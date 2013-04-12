package allocateids;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyRange;

@SuppressWarnings("serial")
public class AllocateIDsServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();
        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");

        DatastoreService ds = DatastoreServiceFactory.getDatastoreService();

        KeyRange range = ds.allocateIds("Entity", 1);
        Key e1Key = range.getStart();
        Entity e1 = new Entity(e1Key);
        Entity e2 = new Entity("Entity");
        e2.setProperty("reference", e1Key);
        ds.put(new ArrayList<Entity>(Arrays.asList(e1, e2)));

        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
