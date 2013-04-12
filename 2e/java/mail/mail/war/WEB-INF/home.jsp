<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
  <head>
    <title>Mail Demo</title>
  </head>
  <body>
<c:choose>
  <c:when test="${emailSuccess}">
    <p>An email has been sent to your address (${user.email}).</p>  </c:when>
  <c:otherwise>
    <p>There was an error sending email.  See the message log.</p>
  </c:otherwise>
</c:choose>

<c:choose>
  <c:when test="${isDevelopment}">
    <p>You are running on the development server. You can use <a href="/_ah/admin/inboundmail">the development server console</a> to send email to this application.</p>
  </c:when>
  <c:otherwise>
    <p>You are running on App Engine.  You can <a href="mailto:${appEmailAddress}">send email to ${appEmailAddress}</a> to send a message to the application.</p>
  </c:otherwise>
</c:choose>

  </body>
</html>
