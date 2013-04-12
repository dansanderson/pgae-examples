package memcache;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;

import com.google.appengine.api.memcache.Expiration;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheService.SetPolicy;
import com.google.appengine.api.memcache.MemcacheServiceFactory;
import com.google.appengine.api.memcache.Stats;
import com.google.appengine.api.memcache.StrictErrorHandler;

@SuppressWarnings("serial")
public class MemcacheDemoServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        List<String> headlines =
            new ArrayList(Arrays.asList("...", "...", "..."));

        MemcacheService memcache = MemcacheServiceFactory.getMemcacheService();

        memcache.put("headlines", headlines);

        headlines = (List<String>) memcache.get("headlines");

        memcache.delete("headlines");

        memcache.put("headlines", headlines,
                     Expiration.byDeltaSeconds(300));

        memcache.put("headlines", headlines, null,
                     SetPolicy.ADD_ONLY_IF_NOT_PRESENT);

        boolean headlinesAreCached = memcache.contains("headlines");

        memcache.put("tempnode91512", "...");
        memcache.delete("tempnode91512", 5);
        memcache.put("tempnode91512", "..."); // fails within the 5 second add-lock

        Map<Object, Object> articleSummaries = new HashMap<Object, Object>();
        articleSummaries.put("article00174", "...");
        articleSummaries.put("article05234", "...");
        articleSummaries.put("article15280", "...");
        memcache.putAll(articleSummaries);

        List<Object> articleSummaryKeys = Arrays.<Object>asList(
            "article00174",
            "article05234",
            "article15820");
        articleSummaries = memcache.getAll(articleSummaryKeys);

        memcache.deleteAll(articleSummaryKeys);

        memcache.setNamespace("News");
        memcache.put("headlines", headlines);

        List<String> userHeadlines =
            new ArrayList(Arrays.asList("...", "...", "..."));
        memcache.setNamespace("User");
        memcache.put("headlines", userHeadlines);

        // Get User:"headlines"
        userHeadlines = (List<String>) memcache.get("headlines");

        // Get News:"headlines"
        memcache.setNamespace("News");
        headlines = (List<String>) memcache.get("headlines");

        memcache.put("work_done", 0);

        Long workDone = memcache.increment("work_done", 1);

        Stats stats = memcache.getStatistics();
        int ageOfOldestItemMillis = stats.getMaxTimeWithoutAccess();

        memcache.setErrorHandler(new StrictErrorHandler());

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
