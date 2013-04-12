package tasks;

import java.io.IOException;
import java.util.logging.Logger;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class TaskServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(TaskServlet.class.getName());

    public void doPost(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        if (req.getParameter("address") == null) {
            log.info("Task ran, no parameters");
        } else {
            log.info("Task ran, address = " + req.getParameter("address") +
                     ", firstname = " + req.getParameter("firstname"));
        }
    }
}
