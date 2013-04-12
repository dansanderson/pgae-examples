package xmpp;

import java.io.IOException;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.servlet.http.*;
import com.google.appengine.api.xmpp.Message;
import com.google.appengine.api.xmpp.MessageBuilder;
import com.google.appengine.api.xmpp.SendResponse;
import com.google.appengine.api.xmpp.XMPPService;
import com.google.appengine.api.xmpp.XMPPServiceFactory;


public class XMPPReceiverServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(XMPPReceiverServlet.class.getName());

    private String doArithmetic(String question) {
        Pattern exprPat = Pattern.compile("\\s*(-?\\d+(?:\\.\\d+)?)\\s*([\\+\\-\\*\\/])\\s*(-?\\d+(?:\\.\\d+)?)");
        Matcher m = exprPat.matcher(question);
        if (!m.matches()) {
            return null;
        }
        Float first = Float.valueOf(m.group(1));
        String op = m.group(2);
        Float second = Float.valueOf(m.group(3));
        Float answer = 0f;
        if (op.equals("+")) {
            answer = first + second;
        } else if (op.equals("-")) {
            answer = first - second;
        } else if (op.equals("*")) {
            answer = first * second;
        } else { // op.equals("/")
            if (second == 0) {
                return "Inf";
            } else {
                answer = first / second;
            }
        }
        return answer.toString();
    }

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp)
        throws IOException {
        XMPPService xmpp = XMPPServiceFactory.getXMPPService();
        Message message = xmpp.parseMessage(req);

        String answer = doArithmetic(message.getBody());
        if (answer == null) {
            answer = "I didn't understand: " + message.getBody();
        }

        Message reply = new MessageBuilder()
            .withRecipientJids(message.getFromJid())
            .withBody(answer)
            .build();
        SendResponse success = xmpp.sendMessage(reply);
        if (success.getStatusMap().get(message.getFromJid())
            != SendResponse.Status.SUCCESS) {
            log.warning("Could not send XMPP reply to " + message.getFromJid());
        }
    }
}
