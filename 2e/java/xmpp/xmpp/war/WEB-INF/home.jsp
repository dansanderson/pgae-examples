<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<html>
  <head>
    <title>XMPP Demo</title>
    <style>
body {
  font-family: sans-serif;
  font-size: 14px;
}

#admin_message {
  padding: 0.5em 1em;
  border: 1px solid #ccc;
}
.hidden {
  display: none;
}

table {
  border: 1px solid #ccc;
  width: 100%;
  margin-bottom: 1em;
}
table th {
  text-align: left;
  font-size: 12px;
  background: #05c;
  color: white;
  padding: 0.5em 1em 0.5em 0.5em;
}
table td {
  padding: 0.2em 1em 0.2em 0.5em;
}

.chat { color: #060; }
.away { color: #660; }
.dnd { color: #600; }
.xa { color: #300; }

    </style>

  </head>
  <body>

<p>Welcome, ${user.email}!  The time is ${currentTime}.  You can <a href="${signoutUrl}">sign in as a different user</a>.</p>

<c:choose>
  <c:when test="${isUserAdmin}">

    <c:if test="${adminMessage != null}">
      <div id="admin_message">${fn:escapeXml(adminMessage)}  <a href="#" onclick="document.getElementById('admin_message').classList.add('hidden');">Dismiss</a></div>
    </c:if>

    <c:choose>
      <c:when test="${isDevelopment}">
        <p>You are running on the development server.  You can use <a href="/_ah/admin/xmpp">the development server console</a> to send an XMPP chat message to this application.  <i>Be sure to use <b>${appId}@appspot.com</b> or <b>anything@${appId}.appspotchat.com</b> as the "To" address.</i></p>
      </c:when>
      <c:otherwise>
        <p>You are running on App Engine.  You can send an XMPP chat message to <b>${appXmppAddress}</b> to communicate with this application.</p>
      </c:otherwise>
    </c:choose>

  <h2>Users</h2>
  <c:if test="${hasChatUsers}">
  <form action="/update" method="post">
    <input type="hidden" name="command" value="clear_users" />
    <input type="submit" value="Clear User Records" />
  </form>
  </c:if>

  <form action="/update" method="post">
  <c:choose>
    <c:when test="${hasChatUsers}">
      <table>
        <tr>
          <th></th>
          <th>JID</th>
          <th>Accepted invitation?</th>
          <th>Subscribed to app?</th>
          <th>Status</th>
          <th>GTalk Presence?</th>
          <th width="40%">Last Chat Message</th>
        </tr>

      <c:forEach var="chatUser" items="${chatUsers}" varStatus="row">
        <tr>
          <td><input name="jid" type="radio" value="${chatUser.properties.jid}" ${row.first ? 'checked' : ''} /></td> 
          <td>${chatUser.properties.jid}</td>
          <td>${chatUser.properties.accepted_invitation}</td>
          <td>${chatUser.properties.is_subscribed}</td>
          <td>
            <c:choose>
              <c:when test="${chatUser.properties.is_available}">
                <span class="${chatUser.properties.presence_show}">${chatUser.properties.presence_show}</span>
                <span>${fn:escapeXml(chatUser.properties.status_message)}</span>
              </c:when>
              <c:otherwise>
                unavailable
              </c:otherwise>
            </c:choose>
          </td>
          <td><!-- TODO: chatUser._gtalk_presence --></td>
          <td>${fn:escapeXml(chatUser.properties.last_chat_message)}</td>
        </tr>
      </c:forEach>
      <tr>
        <td><input name="jid" type="radio" value="" /></td>
        <td colspan="6">...or enter a JID: <input name="jid_other" type="text" value="" width="100px" /></td>
      </tr>
    </table>
    </c:when>
    <c:otherwise>
      <p>There has not yet been any chat activity.</p>
      <p>
        <input name="jid" type="hidden" value="" />
        <label for="jid_other">Enter a JID:</label>
        <input name="jid_other" type="text" value="" width="100px" />
      </p>
    </c:otherwise>
  </c:choose>
    <p>
      <input name="command" type="radio" value="chat" checked /> Send a chat message:<br />
      <textarea name="chat_message" cols="60" rows="4"></textarea><br />
      <input name="command" type="radio" value="invite" /> Invite to chat<br />
      <input name="command" type="radio" value="probe" /> Probe for presence
    </p>
    <input type="submit" value="Make Request" />
  </form>

  <h2>App Presence</h2>
  <p>
    The app presence is currently set to
    <b><c:choose><c:when test="${status.properties.presence_available}">available</c:when><c:otherwise>unavailable</c:otherwise></c:choose></b>
    and <b>${status.properties.presence_show}</b>, "${fn:escapeXml(status.properties.status_message)}".
  </p>
  <form action="/update" method="post">
    <input name="command" type="hidden" value="presence" />

    <p><label for="presence_available">Set availability:</label><br />
    <input name="presence_available" type="radio" value="true" <c:if test="${status.properties.presence_available}">checked </c:if> /> available<br />
    <input name="presence_available" type="radio" value="false" <c:if test="${!status.properties.presence_available}">checked </c:if> /> unavailable<br />
    </p>

    <p><label for="presence_show">Set status:</label><br />
    <input name="presence_show" type="radio" value="chat" <c:if test='${status.properties.presence_show == "chat"}'>checked </c:if> /> chat<br />
    <input name="presence_show" type="radio" value="away" <c:if test='${status.properties.presence_show == "away"}'>checked </c:if> /> away<br />
    <input name="presence_show" type="radio" value="dnd" <c:if test='${status.properties.presence_show == "dnd"}'>checked </c:if> /> do not disturb<br />
    <input name="presence_show" type="radio" value="xa" <c:if test='${status.properties.presence_show == "xa"}'>checked </c:if> /> extended away<br />
    </p>

    <p><label for="status_message">Status message:</label> <input name="status_message" value="" width="100px" /></p>

    <input type="submit" value="Make Request" />
  </form>

  <h2>Last Error</h2>
  <c:choose>
    <c:when test="${status.properties.last_error}">
      <p>Last error:</p>
      <pre>${status.properties.last_error}</pre>
      <p>Received: ${status.properties.last_error_datetime}</p>
    </c:when>
    <c:otherwise>
      <p>The app has not yet received an error XMPP message.</p>
    </c:otherwise>
  </c:choose> 

  </c:when>

  <c:otherwise>
  <p>You must be signed in as an administrator to use the control panel.</p>
  </c:otherwise>
</c:choose>

  </body>
</html>
