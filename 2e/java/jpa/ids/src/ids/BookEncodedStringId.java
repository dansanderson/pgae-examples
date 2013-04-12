package ids;

import java.util.Date;
import javax.persistence.Basic;
import javax.persistence.Entity;
// import javax.persistence.GeneratedValue;
// import javax.persistence.GenerationType;
import javax.persistence.Id;
import org.datanucleus.jpa.annotations.Extension;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;

@Entity(name = "BookEncodedStringId")
public class BookEncodedStringId {
    // Encoded String ID field: objects of this class represent the
    // entity key as an encoded String, making the class portable to
    // other data backends.  Key values can be encoded and decoded
    // using the KeyFactory.keyToString() and stringToKey() methods.
    // Without a @GeneratedValue annotation, the Key value (prior to
    // encoding) must contain an app-assigned key name (a String).
    // With a @GeneratedValue annotation, the datastore assigns a
    // numeric system ID when the object is saved.  The key name or
    // system ID is contained in the (encoded) Key value.
    @Id
    @Extension(vendorName = "datanucleus",
               key = "gae.encoded-pk",
               value = "true")
    // @GeneratedValue(strategy = GenerationType.IDENTITY)    
    private String encodedKeyString;

    // With string-encoded keys, an entity group parent is represented
    // as a separate encoded field.  Its value is the encoded key of
    // the parent.
    @Basic
    @Extension(vendorName = "datanucleus",
               key = "gae.parent-pk",
               value = "true")
    private String parentEncodedKeyString;

    private String title;
    private String author;
    private int copyrightYear;
    private Date authorBirthdate;

    public BookEncodedStringId(Key encodedKey) {
        this.encodedKeyString = KeyFactory.keyToString(encodedKey);
        this.parentEncodedKeyString = null;
    }
    public BookEncodedStringId(String encodedKeyString) {
        this.encodedKeyString = encodedKeyString;
        this.parentEncodedKeyString = null;
    }
    public BookEncodedStringId(Key encodedKey,
                               Key parentEncodedKey) {
        this.encodedKeyString = KeyFactory.keyToString(encodedKey);
        this.parentEncodedKeyString = KeyFactory.keyToString(parentEncodedKey);
    }
    public BookEncodedStringId(String encodedKeyString,
                               String parentEncodedKeyString) {
        this.encodedKeyString = encodedKeyString;
        this.parentEncodedKeyString = parentEncodedKeyString;
    }

    public Key getEncodedKey() {
        return KeyFactory.stringToKey(encodedKeyString);
    }
    public String getEncodedKeyString() {
        return encodedKeyString;
    }
    public Key getParentEncodedKey() {
        if (parentEncodedKeyString == null) {
            return null;
        } else {
            return KeyFactory.stringToKey(parentEncodedKeyString);
        }
    }
    public String getParentEncodedKeyString() {
        return parentEncodedKeyString;
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
