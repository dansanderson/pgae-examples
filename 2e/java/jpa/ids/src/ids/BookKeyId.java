package ids;

import java.util.Date;
import javax.persistence.Entity;
// import javax.persistence.GeneratedValue;
// import javax.persistence.GenerationType;
import javax.persistence.Id;
import com.google.appengine.api.datastore.Key;

@Entity(name = "BookKeyId")
public class BookKeyId {
    // Key ID field: entities of this class use App Engine Key values
    // as IDs.  Without a @GeneratedValue annotation, the Key value
    // must contain an app-assigned key name (a String).  With
    // a @GeneratedValue annotation, the datastore assigns a numeric system ID
    // when the object is saved.  The key name or system ID is
    // contained in the Key value.  The app can specify an entity
    // group parent for new entities by setting one in the Key value.
    @Id
    // @GeneratedValue(strategy = GenerationType.IDENTITY)    
    private Key id;

    private String title;
    private String author;
    private int copyrightYear;
    private Date authorBirthdate;

    public BookKeyId(Key id) {
        this.id = id;
    }

    public Key getId() {
        return id;
    }

    public void setTitle(String title) {
        this.title = title;
    }
    public String getTitle() {
        return title;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
    public String getAuthor() {
        return author;
    }

    public void setCopyrightYear(int copyrightYear) {
        this.copyrightYear = copyrightYear;
    }
    public int getCopyrightYear() {
        return copyrightYear;
    }

    public void setAuthorBirthdate(Date authorBirthdate) {
        this.authorBirthdate = authorBirthdate;
    }
    public Date getAuthorBirthdate() {
        return authorBirthdate;
    }
}
