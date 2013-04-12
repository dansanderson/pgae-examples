package googleaccounts;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

@SuppressWarnings("serial")
public class AccountStatusServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        UserService userService = UserServiceFactory.getUserService();
        if (userService.isUserLoggedIn()) {
            User user = userService.getCurrentUser();
            out.println("<p>You are signed in as " + user.getNickname() + ". ");
            if (userService.isUserAdmin()) {
                out.println("You are an administrator. ");
            }
            out.println("<a href=\"" + userService.createLogoutURL("/") +
                        "\">Sign out</a>.</p>");
        } else {
            out.println("<p>You are not signed in to Google Accounts. " +
                        "<a href=\"" +
                        userService.createLoginURL(req.getRequestURI()) +
                        "\">Sign in</a>.</p>");
        }

        out.println("<ul>" +
                    "<li><a href=\"/\">/</a></li>" +
                    "<li><a href=\"/required\">/required</a></li>" +
                    "<li><a href=\"/admin\">/admin</a></li>" +
                    "</ul>");

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
