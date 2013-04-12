package urlfetch;

import com.google.appengine.api.urlfetch.FetchOptions;
import com.google.appengine.api.urlfetch.HTTPMethod;
import com.google.appengine.api.urlfetch.HTTPRequest;
import com.google.appengine.api.urlfetch.HTTPResponse;
import com.google.appengine.api.urlfetch.ResponseTooLargeException;
import com.google.appengine.api.urlfetch.URLFetchService;
import com.google.appengine.api.urlfetch.URLFetchServiceFactory;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class URLFetchServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        try {
            URL url = new URL("http://ae-book.appspot.com/blog/atom.xml/");

            FetchOptions options = FetchOptions.Builder
                .doNotFollowRedirects()
                .disallowTruncate();
            HTTPRequest request = new HTTPRequest(url, HTTPMethod.GET, options);

            URLFetchService service = URLFetchServiceFactory.getURLFetchService();
            HTTPResponse response = service.fetch(request);

            byte[] content = response.getContent();
            out.println("<p>Read PGAE blog feed (" + content.length + " characters).</p>");

        } catch (ResponseTooLargeException e) {
            out.println("<p>ResponseTooLargeException: " + e + "</p>");

        } catch (MalformedURLException e) {
            out.println("<p>MalformedURLException: " + e + "</p>");

        } catch (IOException e) {
            out.println("<p>IOException: " + e + "</p>");
        }

        out.println("<p>Try <a href=\"/urlconnection\">/urlconnection</a>.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
