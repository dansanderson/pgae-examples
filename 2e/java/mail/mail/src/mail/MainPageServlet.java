package mail;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Logger;
import java.util.Properties;
import java.util.SimpleTimeZone;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Part;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.*;

import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import com.google.appengine.api.utils.SystemProperty;
import com.google.apphosting.api.ApiProxy;

@SuppressWarnings("serial")
public class MainPageServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MainPageServlet.class.getName());

    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException, ServletException { 

        UserService userService = UserServiceFactory.getUserService();
        User user = userService.getCurrentUser();
        String recipientAddress = user.getEmail();

        String appId = ApiProxy.getCurrentEnvironment().getAppId();
        if (appId.startsWith("s~")) {
            appId = appId.substring(2);
        }
        String appEmailAddress = "support@" +
            appId + ".appspotmail.com";

        Properties props = new Properties();
        Session session = Session.getDefaultInstance(props, null);

        String messageBody =
            "Thank you for purchasing The Example App, the best\n" +
            "example on the market!  Your registration key is attached\n" +
            "to this email.\n\n" +
            "To install your key, download the attachment, then select\n" +
            "\"Register...\" from the Help menu.  Select the key file, then click\n" +
            "\"Register\".\n\n" +
            "You can download the app at any time from:\n" +
            "  http://www.example.com/downloads/\n\n" +
            "[This is not a real website.]\n\n" +
            "Thanks again!\n\n" +
            "The Example Team\n";

        String htmlMessageBody =
            "<p>Thank you for purchasing The Example App, the best " +
            "example on the market!  Your registration key is attached " +
            "to this email.</p>" +
            "<p>To install your key, download the attachment, then select " +
            "<b>Register...</b> from the <b>Help</b> menu.  Select the key file, then " +
            "click <b>Register</b>.</p>" +
            "<p>You can download the app at any time from:</p>" +
            "<p>" +
            "<a href=\"http://www.example.com/downloads/\">" +
            "http://www.example.com/downloads/" +
            "</a>" +
            "</p>" +
            "<p>[This is not a real website.]</p>" +
            "<p>Thanks again!</p>" +
            "<p>The Example Team<br />" +
            "<img src=\"http://www.example.com/images/logo_email.gif\" /></p>";

        String softwareKeyData = "REGKEY-12345";

        boolean emailSuccess = true;
        try {
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(appEmailAddress,
                                                "The Example Team"));
            message.addRecipient(Message.RecipientType.TO,
                                 new InternetAddress(recipientAddress));
            message.setSubject("Welcome to Example.com!");

            Multipart multipart = new MimeMultipart();

            MimeBodyPart textPart = new MimeBodyPart();
            textPart.setContent(messageBody, "text/plain");
            multipart.addBodyPart(textPart);

            MimeBodyPart htmlPart = new MimeBodyPart();
            htmlPart.setContent(htmlMessageBody, "text/html");
            multipart.addBodyPart(htmlPart);

            String fileName = "example_key.txt";
            String fileType = "text/plain";
            MimeBodyPart attachmentPart = new MimeBodyPart();
            attachmentPart.setContent(softwareKeyData, fileType);
            attachmentPart.setFileName(fileName);
            multipart.addBodyPart(attachmentPart);

            message.setContent(multipart);
            Transport.send(message);

            log.info("Email sent to: " + recipientAddress);

        } catch (AddressException e) {
            log.warning("AddressException: " + e);
            emailSuccess = false;

        } catch (MessagingException e) {
            log.warning("MessagingException: " + e);
            emailSuccess = false;
        }

        req.setAttribute("appEmailAddress", appEmailAddress);
        req.setAttribute("emailSuccess", emailSuccess);
        req.setAttribute("user", user);

        req.setAttribute("isDevelopment", SystemProperty.environment.value() ==
                         SystemProperty.Environment.Value.Development);

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        req.setAttribute("currentTime", fmt.format(new Date()));

        resp.setContentType("text/html");
        RequestDispatcher jsp = req.getRequestDispatcher("/WEB-INF/home.jsp");
        jsp.forward(req, resp);
    }
}
