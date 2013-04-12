package receivingmail;

import java.io.IOException;
import java.util.Properties;
import java.util.logging.Logger;
import javax.mail.Session;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Part;
import javax.mail.internet.MimeMessage;
import javax.servlet.http.*;


public class MailReceiverServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(MailReceiverServlet.class.getName());

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp)
            throws IOException {
        Properties props = new Properties();
        Session session = Session.getDefaultInstance(props, null);

        try {
            MimeMessage message = new MimeMessage(session, req.getInputStream());
            Object content = message.getContent();
            if (content instanceof String) {
                // A plain text body.
                log.info("Received email message from " +
                         message.getSender() +
                         " (" + message.getContentType() + "): " +
                         content);

            } else if (content instanceof Multipart) {
                // A multipart body.
                log.info("Received multi-part email message (" +
                         ((Multipart) content).getCount() + " parts)");
                for (int i = 0; i < ((Multipart) content).getCount(); i++) {
                    Part part = ((Multipart) content).getBodyPart(i);
                    String partText = (String) part.getContent();
                    log.info("Part " + i + ": " +
                             " (" + message.getContentType() + "): " +
                             partText);
                }
            }
        } catch (MessagingException e) {
            log.info("MessagingException: " + e);
        }
    }
}
