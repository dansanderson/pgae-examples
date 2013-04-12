package properties;

import javax.persistence.Embeddable;

// A class that can be used as a JPA embeddable field.  Fields are
// stored as individual properties of the data object that has the
// field, and can be indexed and queried.

@Embeddable
public class Publisher {
    private String name;
    private String mailingAddress;

    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
        return name;
    }

    public void setMailingAddress(String mailingAddress) {
        this.mailingAddress = mailingAddress;
    }
    public String getMailingAddress() {
        return mailingAddress;
    }
}
