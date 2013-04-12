<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
  <head>
    <title>Blobstore Demo</title>
  </head>
  <body>
    <c:choose>
      <c:when test="${user != null}">
        <p>
          Welcome, ${user.email}!
          You can <a href="${logoutUrl}">sign out</a>.
        </p>
        
        <c:choose>
          <c:when test="${hasUploads}">
            <form action="/delete" method="post">
            <p>Your uploads:</p>
            <ul>
              <c:forEach var="upload" items="${uploads}">
                <li>
                  <input type="checkbox" name="delete" value="${upload.uploadKey}" />
                  ${upload.description}
                  <a href="/view?key=${upload.uploadKey}"
                    >${upload.blob.filename}</a>
                </li>
              </c:forEach>
            </ul>
            <input type="submit" value="Delete Selected" />
            </form>
          </c:when>
          <c:otherwise>
            <p>You have no uploads.</p>
          </c:otherwise>
        </c:choose>
        
        <form action="${uploadUrl}" method="post" enctype="multipart/form-data">
          <label for="description">Description:</label>
            <input type="text" name="description" id="description" /><br />
          <label for="upload">File:</label>
            <input type="file" name="upload" multiple="true" /><br />
          <input type="submit" value="Upload File" />
        </form>
      </c:when>
      <c:otherwise>
        <p>
          Welcome! Please
          <a href="${loginUrl}">sign in or register</a> to upload files.
        </p>
      </c:otherwise>
    </c:choose>
  </body>
</html>
