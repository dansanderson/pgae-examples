package relationships;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.ManyToOne;
import com.google.appengine.api.datastore.Key;

@Entity(name = "BookReview")
public class BookReview {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)    
    private Key id;

    private int rating;

    @ManyToOne
    private Book book;

    public void setRating(int rating) {
        this.rating = rating;
    }
    public int getRating() {
        return rating;
    }

    public Book getBook() {
        return book;
    }
}
