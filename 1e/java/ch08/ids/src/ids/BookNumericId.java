package ids;

import java.util.Date;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity(name = "BookNumericId")
public class BookNumericId {
    // Numeric ID field: entities have a numeric system ID assigned by
    // the datastore automatically, and do not have ancestors.
    // The @GeneratedValue annotation is required. (An app cannot
    // assign numeric IDs, only String key names.)
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String author;
    private int copyrightYear;
    private Date authorBirthdate;

    public Long getId() {
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
