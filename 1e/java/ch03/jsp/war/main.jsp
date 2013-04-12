<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.text.SimpleDateFormat" %>
<%@ page import="java.util.Date" %>
<%@ page import="java.util.SimpleTimeZone" %>
<%@ page import="com.google.appengine.api.users.User" %>
<%@ page import="com.google.appengine.api.users.UserService" %>
<%@ page import="com.google.appengine.api.users.UserServiceFactory" %>

<html>
  <head>
    <title>My Web App</title>
  </head>
  <body>

<%
    SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSSSSS");
    fmt.setTimeZone(new SimpleTimeZone(0, ""));

    UserService userService = UserServiceFactory.getUserService();
    User user = userService.getCurrentUser();
    if (user != null) {
%>
<p>Welcome, <%= user.getNickname() %>! You can
<a href="<%= userService.createLogoutURL(request.getRequestURI()) %>">sign out</a>.</p>
<%
    } else {
%>
<p>Welcome!
<a href="<%= userService.createLoginURL(request.getRequestURI()) %>">Sign in or register</a>
to customize.</p>
<%
    }
%>

<p>This page is built by main.jsp.</p>

<p>The time is: <%= fmt.format(new Date()) %></p>

  </body>
</html>
