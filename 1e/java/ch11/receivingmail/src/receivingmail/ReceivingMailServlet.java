package receivingmail;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;
import com.google.appengine.api.utils.SystemProperty;
import com.google.apphosting.api.ApiProxy;

@SuppressWarnings("serial")
public class ReceivingMailServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        if (SystemProperty.environment.value() ==
            SystemProperty.Environment.Value.Development) {
            out.println("<p>You are running on the development server. " +
                        "You can use <a href=\"/_ah/admin/inboundmail\">" +
                        "the development server console</a> to send email " +
                        "to this application.</p>");

        } else {
            String appId = ApiProxy.getCurrentEnvironment().getAppId();
            String appEmailAddress = "support@" +
                appId + ".appspotmail.com";
            out.println("<p>You are running on App Engine.  You can " +
                        "<a href=\"mailto:" + appEmailAddress + "\">" +
                        "send email to " + appEmailAddress+ "</a> to " +
                        "send a message to the application.</p>");
        }

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
