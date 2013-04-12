package properties;

import java.io.Serializable;
import java.util.Date;

// A Serializable class that can be a field type, stored as a
// datastore blob property value (not indexed).  There are no special
// JPA annotations needed for this; any Serializable class will work.

public class PublisherMetadata implements Serializable {
    private String itemCode;
    private Date productionStartDate;
    private Date productionEndDate;

    public void setItemCode(String itemCode) {
        this.itemCode = itemCode;
    }
    public String getItemCode() {
        return itemCode;
    }

    public void setProductionStartDate(Date productionStartDate) {
        this.productionStartDate = productionStartDate;
    }
    public Date getProductionStartDate() {
        return productionStartDate;
    }

    public void setProductionEndDate(Date productionEndDate) {
        this.productionEndDate = productionEndDate;
    }
    public Date getProductionEndDate() {
        return productionEndDate;
    }
}
