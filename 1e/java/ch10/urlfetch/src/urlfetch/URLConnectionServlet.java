package urlfetch;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class URLConnectionServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        try {
            URL url = new URL("http://ae-book.appspot.com/blog/atom.xml/");
            InputStream inStream = url.openStream();

            InputStreamReader inStreamReader = new InputStreamReader(inStream);
            BufferedReader reader = new BufferedReader(inStreamReader);

            // A useless use of the data just to prove it was read.
            int length = 0;
            while (reader.read() != -1) {
                length++;
            }
            out.println("<p>Read PGAE blog feed (" + length + " characters).</p>");

            reader.close();

        } catch (MalformedURLException e) {
            out.println("<p>MalformedURLException: " + e + "</p>");

        } catch (IOException e) {
            out.println("<p>IOException: " + e + "</p>");
        }

        out.println("<p>Try <a href=\"/urlfetch\">/urlfetch</a>.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
