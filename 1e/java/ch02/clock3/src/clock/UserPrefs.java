package clock;

import javax.persistence.Basic;
import javax.persistence.Entity;
import javax.persistence.EntityManager;
import javax.persistence.Id;
import com.google.appengine.api.users.User;

import clock.EMF;
import clock.UserPrefs;

@Entity(name = "UserPrefs")
public class UserPrefs {
    @Id
    private String userId;

    private int tzOffset;
    
    @Basic
    private User user;

    public UserPrefs(String userId) {
        this.userId = userId;
    }

    public String getUserId() {
        return userId;
    }

    public int getTzOffset() {
        return tzOffset;
    }

    public void setTzOffset(int tzOffset) {
        this.tzOffset = tzOffset;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public static UserPrefs getPrefsForUser(User user) {
        UserPrefs userPrefs = null;

        EntityManager em = EMF.get().createEntityManager();
        try {
            userPrefs = em.find(UserPrefs.class, user.getUserId());
            if (userPrefs == null) {
                userPrefs = new UserPrefs(user.getUserId());
                userPrefs.setUser(user);
            }
        } finally {
            em.close();
        }

        return userPrefs;
    }

    public void save() {
        EntityManager em = EMF.get().createEntityManager();
        try {
            em.merge(this);
        } finally {
            em.close();
        }
    }
}
