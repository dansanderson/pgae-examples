package environment;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.Enumeration;
import java.util.Map;
import java.util.Properties;
import java.util.SimpleTimeZone;
import javax.servlet.http.*;
import com.google.appengine.api.utils.SystemProperty;

@SuppressWarnings("serial")
public class PrintEnvironmentServlet extends HttpServlet {
    public static String escapeHtmlChars(String inStr) {
        return inStr.replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;");
    }

    public static void printDirectoryListing(PrintWriter out,
                                             File dir,
                                             String indent) {
        if (dir.isDirectory()) {
            out.println(indent + escapeHtmlChars(dir.getName()) + "/");
            String[] contents = dir.list();
            for (int i = 0; i < contents.length; i++) {
                printDirectoryListing(out,
                                      new File(dir, contents[i]),
                                      indent + "  ");
            }
        } else {
            out.println(indent + escapeHtmlChars(dir.getName()));
        }
    }

    public void doPost(HttpServletRequest req,
                       HttpServletResponse resp) 
        throws IOException {
        doGet(req, resp);
    }

    public void doGet(HttpServletRequest req,
                      HttpServletResponse resp)
        throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        String[] nameArray;

        out.println("<ul>" +
                    "<li><a href=\"#env\">Environment Variables</a></li>" +
                    "<li><a href=\"#props\">System Properties</a></li>" +
                    "<li><a href=\"#filesystem\">File System</a></li>" +
                    "<li><a href=\"#request\">Request Data</a></li>" +
                    "</ul>");

        out.println("<hr noshade><h2 id=\"servlet\">Servlet Information</h2><table>");
        out.println("<tr><td valign=\"top\">this.getServletContext().getServerInfo()</td>" +
                    "<td valign=\"top\">" +
                    escapeHtmlChars(this.getServletContext().getServerInfo()) +
                    "</td></tr>");
        out.println("<tr><td>SystemProperty.environment</td>");
        if (SystemProperty.environment.value() == SystemProperty.Environment.Value.Production) {
            out.println("<td>SystemProperty.Environment.Value.Production</td>");
        } else {
            out.println("<td>SystemProperty.Environment.Value.Development</td>");
        }
        out.println("</tr>");
        out.println("<tr><td>SystemProperty.version</td><td><code>" + escapeHtmlChars(SystemProperty.version.get()) + "</code></td></tr>");
        out.println("</table>");
        // TODO: servlet context attributes
        // TODO: servlet context init parameters

        out.println("<hr noshade><h2 id=\"env\">Environment Variables</h2><table>");
        Map<String, String> environment = System.getenv();
        nameArray = environment.keySet().toArray(new String[] {});
        Arrays.sort(nameArray);
        for (String name : nameArray) {
            out.println("<tr><td valign=\"top\"><code>" + escapeHtmlChars(name) +
                        "</code></td><td valign=\"top\"><code>" +
                        escapeHtmlChars(environment.get(name)) + "</code></td></tr>");
        }
        out.println("</table>");

        out.println("<hr noshade><h2 id=\"props\">System Properties</h2><table>");
        Properties systemProperties = System.getProperties();
        nameArray = Collections.list(systemProperties.propertyNames()).toArray(new String[] {});
        Arrays.sort(nameArray);
        for (String name : nameArray) {
            out.println("<tr><td valign=\"top\"><code>" + escapeHtmlChars(name) +
                        "</code></td><td valign=\"top\"><code>" +
                        escapeHtmlChars(systemProperties.getProperty(name)) + "</code></td></tr>");
        }
        out.println("</table>");

        out.println("<hr noshade><h2 id=\"filesystem\">File System</h2><pre>");
        printDirectoryListing(out, new File("."), "");
        out.println("</pre>");

        out.println("<hr noshade><h2 id=\"request\">Request Data</h2><pre>");
        BufferedReader reader = req.getReader();
        String line;
        while ((line = reader.readLine()) != null) {
            out.println(escapeHtmlChars(line));
        }
        out.println("</pre>");
        // TODO: servlet request attributes
        // TODO: request parameters

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
        fmt.setTimeZone(new SimpleTimeZone(0, ""));
        out.println("<hr noshade><p>The time is: " + fmt.format(new Date()) + "</p>");
    }
}
