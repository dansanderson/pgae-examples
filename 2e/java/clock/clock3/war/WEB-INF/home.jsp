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
    <c:if test="${user != null}">
      <form action="/prefs" method="post">
        <label for="tz_offset">
          Timezone offset from UTC (can be negative):
        </label>
        <input name="tz_offset" id="tz_offset" type="text"
          size="4" value="${tzOffset}" />
        <input type="submit" value="Set" />
      </form>
    </c:if>
  </body>
</html>
