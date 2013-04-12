package sendingmail;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.SimpleTimeZone;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
import javax.servlet.http.*;

import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserServiceFactory;


@SuppressWarnings("serial")
public class SendingMailServlet extends HttpServlet {
    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        User user = UserServiceFactory.getUserService().getCurrentUser();
        String recipientAddress = user.getEmail();

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

        try {
            // Replace "admin@example.com" with the email address of a
            // Google Account registered as a developer for this
            // app.
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress("admin@example.com",
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

            out.println("<p>Email sent to " + recipientAddress + ".</p>");

        } catch (AddressException e) {
            out.println("<p>AddressException: " + e + "</p>");

        } catch (MessagingException e) {
            out.println("<p>MessagingException: " + e + "</p>");
        }

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
