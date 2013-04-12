package tasks;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;
import com.google.appengine.api.taskqueue.Queue;
import com.google.appengine.api.taskqueue.QueueFactory;
import com.google.appengine.api.taskqueue.TaskOptions;

@SuppressWarnings("serial")
public class TaskEnqueueServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        Queue queue = QueueFactory.getDefaultQueue();
        queue.add();
        queue.add();
        queue.add();
        out.println("<p>Enqueued 3 tasks to the default queue.</p>");

        TaskOptions taskOptions =
            TaskOptions.Builder.withUrl("/send_invitation_task")
            .param("address", "juliet@example.com")
            .param("firstname", "Juliet");
        queue.add(taskOptions);
        out.println("<p>Enqueued 1 task to the default queue with parameters.</p>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
