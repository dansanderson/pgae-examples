package blobstoredemo;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.blobstore.BlobInfoFactory;
import com.google.appengine.api.blobstore.BlobKey;
import com.google.appengine.api.blobstore.BlobstoreService;
import com.google.appengine.api.blobstore.BlobstoreServiceFactory;
import com.google.appengine.api.blobstore.UploadOptions;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

@SuppressWarnings("serial")
public class MainPageServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException, ServletException {

        UserService userService = UserServiceFactory.getUserService();
        User user = userService.getCurrentUser();
        String loginUrl = userService.createLoginURL("/");
        String logoutUrl = userService.createLogoutURL("/");

        BlobstoreService blobstoreService =
                BlobstoreServiceFactory.getBlobstoreService();
        UploadOptions uploadOptions = UploadOptions.Builder
                .withMaxUploadSizeBytesPerBlob(1024L * 1024L * 1024L)
                .maxUploadSizeBytes(10L * 1024L * 1024L * 1024L);
        String uploadUrl = blobstoreService.createUploadUrl("/upload", uploadOptions);

        DatastoreService ds = DatastoreServiceFactory.getDatastoreService();
        BlobInfoFactory blobInfoFactory = new BlobInfoFactory();
        List<Map<String, Object>> uploads = new ArrayList<Map<String, Object>>();

        Key userGroupKey = KeyFactory.createKey("UserUploadGroup", user.getEmail());
        Query q = new Query("UserUpload").setAncestor(userGroupKey);
        q.addFilter("user", Query.FilterOperator.EQUAL, user);
        PreparedQuery pq = ds.prepare(q);
        Iterable<Entity> results = pq.asIterable();
        for (Entity result : results) {
            Map<String, Object> upload = new HashMap<String, Object>();
            upload.put("description", (String) result.getProperty("description"));
            BlobKey blobKey = (BlobKey) result.getProperty("upload");
            upload.put("blob", blobInfoFactory.loadBlobInfo(blobKey));
            upload.put("uploadKey", KeyFactory.keyToString(result.getKey()));
            uploads.add(upload);
        }
                
        req.setAttribute("user", user);
        req.setAttribute("loginUrl", loginUrl);
        req.setAttribute("logoutUrl", logoutUrl);
        req.setAttribute("uploadUrl", uploadUrl);
        req.setAttribute("uploads", uploads);
        req.setAttribute("hasUploads", !uploads.isEmpty());

        resp.setContentType("text/html");
        
        RequestDispatcher jsp = req.getRequestDispatcher("/WEB-INF/home.jsp");
        jsp.forward(req, resp);
    }
}
