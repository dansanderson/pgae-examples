package transactions;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import javax.persistence.Entity;
import javax.persistence.Id;

import transactions.BookReview;

@Entity(name = "Book")
public class Book {
    @Id
    private String isbn;

    private String title;
    private String author;
    private int copyrightYear;
    private Date authorBirthdate;
    private List<BookReview> bookReviews = null;

    public Book(String isbn) {
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

    public void setBookReviews(List<BookReview> bookReviews) {
        this.bookReviews = bookReviews;
    }
    public List<BookReview> getBookReviews() {
        if (bookReviews == null) {
            bookReviews = new ArrayList<BookReview>();
        }
        return bookReviews;
    }
}
