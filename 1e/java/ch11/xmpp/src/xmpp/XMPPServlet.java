package xmpp;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;
import com.google.appengine.api.utils.SystemProperty;
import com.google.apphosting.api.ApiProxy;

@SuppressWarnings("serial")
public class XMPPServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        String appId = ApiProxy.getCurrentEnvironment().getAppId();

        if (SystemProperty.environment.value() ==
            SystemProperty.Environment.Value.Development) {
            out.println("<p>You are running on the development server. " +
                        "You can use <a href=\"/_ah/admin/xmpp\">the " +
                        "development server console</a> to send an XMPP " +
                        "chat message to this application.</p>" +
                        "<p><i>Be sure to use <b>" + appId +
                        "@appspot.com</b> or <b>anything@" + appId +
                        ".appspotchat.com</b> as the \"To\" address.</i></p>");
        } else {
            out.println("<p>You are running on App Engine.  You can " +
                        "send an XMPP chat message to " + appId +
                        "@appspot.com to communicate with this application.</p>");
        }

        out.println("<p>This app responds to messages that contain simple " +
                    "two-term arithmetic expressions, such as <code>2 + 3</code> " +
                    "or <code>144 / 4</code>.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
