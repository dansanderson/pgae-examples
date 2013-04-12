package blobstoredemo;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.appengine.api.blobstore.BlobKey;
import com.google.appengine.api.blobstore.BlobstoreService;
import com.google.appengine.api.blobstore.BlobstoreServiceFactory;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.EntityNotFoundException;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

@SuppressWarnings("serial")
public class ViewUploadServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
            HttpServletResponse resp)
            throws IOException {
        UserService userService = UserServiceFactory.getUserService();
        User user = userService.getCurrentUser();
        DatastoreService ds = DatastoreServiceFactory.getDatastoreService();
        BlobstoreService bs =
                BlobstoreServiceFactory.getBlobstoreService();

        String uploadKeyStr = req.getParameter("key");
        Entity userUpload = null;
        BlobKey blobKey = null;
        if (uploadKeyStr != null) {
            try {
                userUpload = ds.get(KeyFactory.stringToKey(uploadKeyStr));
                if (((User)userUpload.getProperty("user")).equals(user)) {
                    blobKey = (BlobKey)userUpload.getProperty("upload");
                }
            } catch (EntityNotFoundException e) {
                // Leave blobKey null.
            }
        }
        
        if (blobKey != null) {
            bs.serve(
                    blobKey,
                    bs.getByteRange(req),
                    resp);
        } else {
            resp.sendError(404);
        }
    }
}
