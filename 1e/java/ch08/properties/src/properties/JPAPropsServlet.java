package properties;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.SimpleTimeZone;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityManager;
import javax.servlet.http.*;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.datastore.KeyFactory.Builder;
import com.google.appengine.api.datastore.ShortBlob;

import properties.Book;
import properties.EMF;

@SuppressWarnings("serial")
public class JPAPropsServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        EntityManagerFactory emf = EMF.get();
        EntityManager em = null;

        try {
            em = emf.createEntityManager();

            Book book = new Book();

            book.setTitle("The Grapes of Wrath");
            book.setAuthor("John Steinbeck");
            book.setCopyrightYear(1939);
            Date authorBirthdate =
                new GregorianCalendar(1902, Calendar.FEBRUARY, 27).getTime();
            book.setAuthorBirthdate(authorBirthdate);

            ShortBlob coverIcon = new ShortBlob(new byte[] { 1, 2, 126, 127 });
            book.setCoverIcon(coverIcon);

            // stored as a multi-valued property
            book.setTags(Arrays.asList("depression", "grapes", "wrath"));

            // not stored (@Transient)
            book.setDebugAccessCount(9999);

            // stored as long_description
            book.setLongDescription("...");

            // stored but not indexed
            book.setFirstSentence("...");

            // Serializable field type stored as a datastore blob property,
            // not indexed
            PublisherMetadata publisherMetadata = new PublisherMetadata();
            publisherMetadata.setItemCode("X1841GH9");
            Date productionStartDate =
                new GregorianCalendar(2002, Calendar.APRIL, 28).getTime();
            publisherMetadata.setProductionStartDate(productionStartDate);
            Date productionEndDate =
                new GregorianCalendar(2002, Calendar.JULY, 7).getTime();
            publisherMetadata.setProductionEndDate(productionEndDate);
            book.setPublisherMetadata(publisherMetadata);

            // JPA embedded object, stored as multiple properties on the
            // Book entity.
            Publisher publisher = new Publisher();
            publisher.setName("GM Classics");
            publisher.setMailingAddress("123 Paper St., Schenectady, NY, 12345");
            book.setPublisher(publisher);

            em.persist(book);

        } finally {
            em.close();
        }

        out.println("<p>Object of kind \"Book\" saved.  See <a href=\"/_ah/admin\">the datastore viewer</a>.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
