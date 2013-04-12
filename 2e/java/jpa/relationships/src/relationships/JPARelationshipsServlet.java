package relationships;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;
import java.util.SimpleTimeZone;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import javax.persistence.Query;
import javax.servlet.http.*;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.datastore.KeyFactory.Builder;

import relationships.Book;
import relationships.BookReview;
import relationships.EMF;

@SuppressWarnings("serial")
public class JPARelationshipsServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        EntityManagerFactory emf = EMF.get();
        EntityManager em = null;

        try {
            em = emf.createEntityManager();

            Book book = new Book("978-0141185064");
            book.setTitle("The Grapes of Wrath");
            book.setAuthor("John Steinbeck");
            book.setCopyrightYear(1939);
            Date authorBirthdate =
                new GregorianCalendar(1902, Calendar.FEBRUARY, 27).getTime();
            book.setAuthorBirthdate(authorBirthdate);

            book.setBookCoverImage(new BookCoverImage());
            book.getBookCoverImage().setType("image/jpg");

            List<BookReview> bookReviews = book.getBookReviews();
            BookReview bookReview = new BookReview();
            bookReview.setRating(5);
            bookReviews.add(bookReview);
            bookReview = new BookReview();
            bookReview.setRating(4);
            bookReviews.add(bookReview);

            EntityTransaction txn = em.getTransaction();
            txn.begin();
            try {
                // When the Book is made persistent, the "PERSIST"
                // action cascades to the BookCoverImage object and
                // all BookReview objects.
                em.persist(book);
                txn.commit();
            } finally {
                if (txn.isActive()) {
                    txn.rollback();
                }
            }

        } finally {
            em.close();
        }

        try {
            em = emf.createEntityManager();

            Book book = em.find(Book.class, "978-0141185064");
            if (book != null) {
                out.println("<p>Found <i>" + book.getTitle() + "</i></p>");

                // Automatically fetch the BookCoverImage entity and access a field.
                out.println("<p>Book cover image type: " + book.getBookCoverImage().getType() + "</p>");

                out.println("<p>Ratings: ");
                for (BookReview bookReview : book.getBookReviews()) {
                    out.println("[" + bookReview.getRating() + "] ");
                }
                out.println("</p>");

            } else {
                out.println("Could not find that book I was looking for...");
            }

        } finally {
            em.close();
        }

        out.println("<p>Objects saved.  See <a href=\"/_ah/admin\">the datastore viewer</a>.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
