package ids;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityManager;
import javax.servlet.http.*;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.datastore.KeyFactory.Builder;

import ids.BookEncodedStringId;
import ids.BookKeyId;
import ids.BookNumericId;
import ids.BookStringId;
import ids.EMF;

@SuppressWarnings("serial")
public class JPAIDsServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        EntityManagerFactory emf = EMF.get();
        EntityManager em = null;

        // TODO: It should be possible to do all of these with one
        // EntityManager with NontransactionalWrite set to true in the
        // persistence.xml configuration, but this doesn't appear to
        // work in SDK 1.3.0.
        // http://code.google.com/p/datanucleus-appengine/issues/detail?id=183

        try {
            em = emf.createEntityManager();

            // An entity with a String key name and no ancestors.
            BookStringId book1 = new BookStringId("978-0-596-52272-8");
            em.persist(book1);

        } finally {
            em.close();
        }

        try {
            em = emf.createEntityManager();

            // An entity with a numeric system ID and no ancestors.
            // System ID is not assigned until the EntityManager is
            // closed in the finally block.
            BookNumericId book2 = new BookNumericId();
            em.persist(book2);

        } finally {
            em.close();
        }

        try {
            em = emf.createEntityManager();

            // An entity with a Key ID field. Can have an ancestor set
            // in the Key.
            Key book3key = new Builder("Publisher", "O'Reilly")
                .addChild("BookKeyId", "978-0-596-52272-8")
                .getKey();
            BookKeyId book3 = new BookKeyId(book3key);
            em.persist(book3);

        } finally {
            em.close();
        }

        try {
            em = emf.createEntityManager();

            // An object with its entity's key encoded as two String
            // fields, one for the object's kind and (string or
            // numeric) ID, and one for the parent.  (The class
            // constructor calls KeyFactory.keyToString() to encode
            // the Key values.  See BookEncodedStringId.java.)
            Key book4keyParent = new Builder("Publisher", "O'Reilly").getKey();
            Key book4key = new Builder("BookEncodedStringId", "978-0-596-52272-8")
                .getKey();
            BookEncodedStringId book4 = new BookEncodedStringId(book4key,
                                                                book4keyParent);
            em.persist(book4);

        } finally {
            em.close();
        }

        out.println("<p>Objects saved.  See <a href=\"/_ah/admin\">the datastore viewer</a>.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
