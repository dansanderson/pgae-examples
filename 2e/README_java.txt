Running the Java Examples
-------------------------

The java/ directory contains examples for Google App Engine's Java
runtime environment.  In order to run a Java example on your computer,
you need the Java 6 SDK, or a later version, and the Google App Engine
Java SDK.  To build the examples using the build scripts provided, you
also need Apache Ant.

You can get the Java 6 SDK from Oracle's website:
  http://www.oracle.com/technetwork/java/javase/downloads/index.html

You can download the App Engine Java SDK as a Zip archive from here:
  http://developers.google.com/appengine/downloads

You can get Apache Ant here:
  http://ant.apache.org/

To build and run a Java example using Ant, change the current working
directory to the root directory of one of the samples.  Use Ant to
build the "runserver" target to build the sample and start the
development server, setting the "sdk.dir" property to the path of your
App Engine SDK:
  cd java/clock/clock1
  ant -Dsdk.dir=/path/to/appengine-java-sdk runserver

(The default "sdk.dir" is a relative path, 5 levels up from the
example's directory.  This is the directory that contains
"pgae-examples" if you clone the Mercurial repository.)

Alternatively, you can use the Eclipse IDE and the Google Plugin for
Eclipse to build and run the examples.  Each App Engine Java app needs
a copy of the App Engine JARs in the final WAR directory.  To save
space in this collection, these JARs have been omitted from the
example directories.  In Eclipse, the easiest way to get a sample
running is to create a new App Engine project, copy the source files
from the example into the project, then run (or debug) the project
from within Eclipse.

You can get the Eclipse IDE from the Eclipse website:
  http://www.eclipse.org/

For instructions on installing the Google Plugin for Eclipse, which
includes the App Engine Java SDK, see the Google Plugin website:
  http://developers.google.com/eclipse/


Uploading the Java Examples to App Engine
-----------------------------------------

Before you can upload a Java example to App Engine, you must edit the
war/WEB-INF/appengine-web.xml file and change the <application> and
<version> elements so they contain the desired application ID and
version ID:
  <?xml version="1.0" encoding="utf-8"?>
  <appengine-web-app xmlns="http://appengine.google.com/ns/1.0">
    <application>APP-ID</application>
    <version>VERSION-ID</version>
    <threadsafe>true</threadsafe>
  </appengine-web-app>

If you're using Ant, build the "update" target to build the project
and attempt to upload the app.  If this is the first time you've
uploaded an app, the upload step will fail with an error message, but
do it anyway to build the project:
  cd java/clock/clock1
  ant update

The "update" target needs you to use the "appcfg update" command
("appcfg.sh update" in Mac OS X or Linux) for the first update so it
can prompt for and store your credentials.  Run this command,
specifying the location of the war/ directory as an argument:
  appcfg update war

"appcfg" prompts you for your Google account email address and
password, and uploads the app.  For future uploads, you can run
"ant update" from the example's root directory to build and upload the
app, and it will use your stored credentials (until they expire).

If you're using Eclipse, you can upload the example by clicking the
App Engine button in the Eclipse toolbar.  Eclipse builds the project,
prompts for your Google Account email address and password, and
uploads the app.

Test the uploaded example by visiting the corresponding appspot.com
URL:
  http://VERSION-ID.APP-ID.appspot.com/

* Note: When you upload an example that performs datastore queries,
  App Engine may need to build indexes requested by the application's
  configuration before it can serve requests for the example
  successfully.  If you get a NeedIndexError, check the Administration
  Console's "Datastore Indexes" to check the status of the index
  building process.


The Java Examples
-----------------

Chapter 2

java/clock/clock1/
    A simple Java app, with a WAR directory structure (war/) and a
    source directory (src/) using a standard layout, and an Apache Ant
    build file with targets for compiling the code and running the
    development server.  The example includes a simple servlet class
    that outputs a dynamic message to the browser.

java/clock/clock2/
    An example with Google Accounts sign-in and sign-out
    functionality.

java/clock/clock3/
    A clock application that prompts a signed-in user for a timezone
    offset to customize the display, and remembers the preference for
    future sessions using the datastore.

java/clock/clock4/
    An improved version of the customizable clock that caches the
    user's preference data using the memcache, resulting in a faster
    user experience.


Chapter 3

java/configuration/environment/
    Prints information about the Java environment, such as environment
    variables, system properties, servlet data, the app server
    filesystem, and the request data.

java/configuration/googleaccounts/
    Configuring Google Accounts authentication, in Java.

java/configuration/logging/
    A simple demonstration of the java.util.logging package.

java/configuration/secureconnections/
    Configuring secure connections, in Java.

java/configuration/staticfiles/
    Configuring static files, in Java.

java/configuration/jsp/
    An example using Java ServerPages (JSPs).


Chapter 5

java/datastore/allocateids/
    Allocating numeric IDs prior to creating entities.

java/datastore/booklowlevel/
    Creating "Book" entities using the low-level datastore API.

java/datastore/bookjpa/
    Creating "Book" entities using JPA.

java/datastore/entities/
    Manipulating datastore entities using the low-level datastore API.

java/datastore/types/
    A demonstration of entity property types, including MVPs.


Chapter 6

java/datastore/queries/
    Using the low-level datastore API to perform queries.


Chapter 7

java/datastore/transactions/
    Performing transactions on entity groups using the low-level datastore API.


Chapter 8

java/remoteapi/remoteapi/
    A simple app with the remote API handler installed.  See also
    python/remoteapi/remoteapi/.


Chapter 10

java/jpa/ids/
    JPA examples illustrating the three different kinds of primary key fields.

java/jpa/properties/
    Examples of property types.

java/jpa/queries/
    Performing queries using JPQL.

java/jpa/relationships/
    Modeling relationships with JPA.

java/jpa/transactions/
    Using transactions with JPA.


Chapter 11

java/memcache/memcache/
    A demonstration of the features of the memcache API.


Chapter 12

java/blobstore/blobstore
    A full demonstration app that accepts user uploads to the
    Blobstore, and allows the user to view and delete the values.


Chapter 13

java/urlfetch/urlfetch/
    Calling the URL Fetch service, using either URLConnection or URLFetchService.


Chapter 14

java/mail/mail/
    Sending and receiving email messages in Java.


Chapter 15

java/xmpp/xmpp/
    A full demonstration app that can send and receive XMPP chat and
    presence messages, in Java.


Chapter 16

java/tasks/cron/
    A simple example of scheduled task (cron) configuration.

java/tasks/tasks/
    A simple example showing how task queues are configured, and how
    tasks are created.
