package loggingtest;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import java.util.logging.Logger;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class LoggingServlet extends HttpServlet {
    private static final Logger log = Logger.getLogger(LoggingServlet.class.getName());

    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        log.finest("finest level");
        log.finer("finer level");
        log.fine("fine level");
        log.config("config level");
        log.info("info level");
        log.warning("warning level");
        log.severe("severe level");

        System.out.println("stdout level");
        System.err.println("stderr level");

        out.println("<p>Messages logged.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
