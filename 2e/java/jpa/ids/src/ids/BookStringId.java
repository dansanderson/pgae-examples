package ids;

import java.util.Date;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity(name = "BookStringId")
public class BookStringId {
    // String ID field: entities of this class use key names set by
    // the app prior to saving, and do not have ancestors (entity
    // group parents).
    @Id
    private String isbn;

    private String title;
    private String author;
    private int copyrightYear;
    private Date authorBirthdate;

    public BookStringId(String isbn) {
        this.isbn = isbn;
    }

    public String getIsbn() {
        return isbn;
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
