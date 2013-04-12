package properties;

import java.util.Date;
import java.util.List;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Transient;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.ShortBlob;
import org.datanucleus.jpa.annotations.Extension;

import properties.Publisher;
import properties.PublisherMetadata;

@Entity(name = "Book")
public class Book {
    // A Key ID with system-assigned numeric IDs.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)    
    private Key id;

    // These fields are automatically considered persistent (@Basic)
    // because their types are described as such in the JPA
    // specification.
    private String title;
    private String author;
    private int copyrightYear;
    private Date authorBirthdate;

    // Datastore native types that are not in the JPA standard must
    // have the @Basic annotation to be considered persistent.
    @Basic
    private ShortBlob coverIcon;

    // Collection fields are stored as multi-valued properties.  Such
    // a field must have the @Basic annotation.
    @Basic
    private List<String> tags;

    // Fields annotated as @Transient are not persisted to the
    // datastore, regardless of their types.
    @Transient
    private int debugAccessCount;

    // By default, the property name is the name of the field.  You
    // can specify the property name manually using @Column.
    @Column(name = "long_description")
    private String longDescription;

    // You can declare that a field should not be indexed by the
    // datastore with a DataNucleus @Extension annotation.
    @Extension(vendorName = "datanucleus",
               key = "gae.unindexed",
               value = "true")
    private String firstSentence;

    // A Serializable object can be stored in a field.  The value is
    // serialized and stored as a datastore blob property value (not
    // indexed).
    @Lob
    private PublisherMetadata publisherMetadata;

    // JPA embedded objects are supported.  See the @Embeddable
    // annotation on the data class.  The embedded class's fields are
    // stored as individual properties of the outer object, and are
    // queryable.
    private Publisher publisher;


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

    public void setCoverIcon(ShortBlob coverIcon) {
        this.coverIcon = coverIcon;
    }
    public ShortBlob getCoverIcon() {
        return coverIcon;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }
    public List<String> getTags() {
        return tags;
    }

    public void setDebugAccessCount(int debugAccessCount) {
        this.debugAccessCount = debugAccessCount;
    }
    public int getDebugAccessCount() {
        return debugAccessCount;
    }

    public void setLongDescription(String longDescription) {
        this.longDescription = longDescription;
    }
    public String getLongDescription() {
        return longDescription;
    }

    public void setFirstSentence(String firstSentence) {
        this.firstSentence = firstSentence;
    }
    public String getFirstSentence() {
        return firstSentence;
    }

    public void setPublisherMetadata(PublisherMetadata publisherMetadata) {
        this.publisherMetadata = publisherMetadata;
    }
    public PublisherMetadata getPublisherMetadata() {
        return publisherMetadata;
    }

    public void setPublisher(Publisher publisher) {
        this.publisher = publisher;
    }
    public Publisher getPublisher() {
        return publisher;
    }
}
