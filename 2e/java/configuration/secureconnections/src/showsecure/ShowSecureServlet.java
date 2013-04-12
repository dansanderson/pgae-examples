package showsecure;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class ShowSecureServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        if (req.getScheme() == "https") {
            out.println("<p>This page was accessed over a secure connection.</p>");
        } else {
            out.println("<p>This page was accessed over a normal (non-secure) connection.</p>");
        }

        String httpNormalUrl = "http://" + req.getServerName() + "/normal";
        String httpsNormalUrl = "https://" + req.getServerName() + "/normal";
        String httpSecureUrl = "http://" + req.getServerName() + "/secure/url";
        String httpsSecureUrl = "https://" + req.getServerName() + "/secure/url";
        out.println("<ul>" +
                    "<li><a href=\"" + httpNormalUrl + "\">" + httpNormalUrl + "</a></li>" +
                    "<li><a href=\"" + httpsNormalUrl + "\">" + httpsNormalUrl + "</a></li>" +
                    "<li><a href=\"" + httpSecureUrl + "\">" + httpSecureUrl + "</a> (redirects to https)</li>" +
                    "<li><a href=\"" + httpsSecureUrl + "\">" + httpsSecureUrl + "</a></li>" +
                    "</ul>");

        out.println("<p>The development server does not support HTTPS, only HTTP.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
