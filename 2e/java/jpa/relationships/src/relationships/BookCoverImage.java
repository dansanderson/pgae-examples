package relationships;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToOne;
import com.google.appengine.api.datastore.Blob;
import com.google.appengine.api.datastore.Key;

@Entity(name = "BookCoverImage")
public class BookCoverImage {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)    
    private Key id;

    private Blob image;
    private String type;

    @OneToOne(mappedBy="bookCoverImage")
    private Book book;

    public void setImage(Blob image) {
        this.image = image;
    }
    public Blob getImage() {
        return image;
    }

    public void setType(String type) {
        this.type = type;
    }
    public String getType() {
        return type;
    }
}
