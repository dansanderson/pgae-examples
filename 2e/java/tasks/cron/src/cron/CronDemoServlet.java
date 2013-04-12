package cron;

import java.io.IOException;
import java.util.logging.Logger;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class CronDemoServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(CronDemoServlet.class.getName());

    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        log.info("Scheduled task ran.");
    }
}
