<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
  <head>
    <title>The Time Is...</title>
  </head>
  <body>
    <c:choose>
      <c:when test="${user != null}">
        <p>
          Welcome, ${user.email}!
          You can <a href="${logoutUrl}">sign out</a>.
        </p>
      </c:when>
      <c:otherwise>
        <p>
          Welcome!
          <a href="${loginUrl}">Sign in or register</a> to customize.
        </p>
      </c:otherwise>
    </c:choose>
    <p>The time is: ${currentTime}</p>
  </body>
</html>
