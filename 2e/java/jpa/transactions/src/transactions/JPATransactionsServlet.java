package transactions;

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

import transactions.Book;
import transactions.BookReview;
import transactions.EMF;

@SuppressWarnings("serial")
public class JPATransactionsServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        EntityManagerFactory emf = EMF.get();
        EntityManager em = null;

        try {
            em = emf.createEntityManager();
            Book book = new Book("978-0596522728");
            book.setTitle("Programming Google App Engine");
            book.setAuthor("Dan Sanderson");
            book.setCopyrightYear(2010);
            Date authorBirthdate =
                new GregorianCalendar(1978, Calendar.JANUARY, 11).getTime();
            book.setAuthorBirthdate(authorBirthdate);

            em.persist(book);
        } finally {
            em.close();
        }

        try {
            em = emf.createEntityManager();

            EntityTransaction txn = em.getTransaction();
            txn.begin();
            try {
                Book book = em.find(Book.class, "978-0596522728");
                BookReview bookReview = new BookReview();
                bookReview.setRating(5);
                book.getBookReviews().add(bookReview);

                // No need to explicitly persist() the BookReview
                // because it is a field of Book.

                // Persist all updates and commit.
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

            Book book = em.find(Book.class, "978-0596522728");
            if (book != null) {
                out.println("<p>Ratings for <i>" + book.getTitle() + "</i>: ");
                for (BookReview review : book.getBookReviews()) {
                    out.println("[" + review.getRating() + "]");
                }
                out.println("</ul>");
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
