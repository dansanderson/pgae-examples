Running the Python Examples
---------------------------

The python/ directory contains examples for Google App Engine's Python
runtime environment.  In order to run a Python example on your
computer, you need Python 2.5 (not 3.x) and the Google App Engine
Python SDK.  Python 2.6 will work, but the tools will print harmless
warnings when you run a command from the SDK.

You can download Python 2.5.x from the Python website:
  http://www.python.org/

You can download the App Engine Python SDK from here:
  http://code.google.com/appengine/downloads.html

To run a Python example, use the "dev_appserver.py" command provided
by the SDK with the example's project directory as the first argument:
  dev_appserver.py python/ch02/clock1

Alternatively, you can run each example from the Launcher app included
in the Windows and Mac OS X versions of the SDK.  To do so, open the
Launcher, select the File menu, Add Existing Application...  Browse to
the example's root directory and select it.  Select the project from
the app list, then click the Run button.


Uploading the Python Examples to App Engine
-------------------------------------------

To upload a Python example to App Engine, run the "appcfg.py update"
command, specifying the application ID, the version ID, and the path
to the example's root directory as arguments:
  appcfg.py update --application=APP-ID --version=VERSION-ID python/ch02/clock1

The --application and --version arguments override the settings in the
example's app.yaml file.  The command prompts you for your Google
account email address and password, and uploads the example.

Test the uploaded example by visiting the corresponding appspot.com
URL:
  http://VERSION-ID.latest.APP-ID.appspot.com/

* Note: When you upload an example that performs datastore queries,
  App Engine may need to build indexes requested by the application's
  configuration before it can serve requests for the example
  successfully.  If you get a NeedIndexError, check the Administration
  Console's "Datastore Indexes" to check the status of the index
  building process.


The Python Examples
-------------------

python/ch02/clock1/
    A simple Python app, with an app.yaml configuration file and a
    main.py request handler script.  The script uses print statements
    to output the HTTP header for the CGI protocol, and a dynamic
    message that appears in the browser.

python/ch02/clock2/
    An example using the webapp web application framework.

python/ch02/clock3/
    An example with Google Accounts sign-in and sign-out
    functionality.

python/ch02/clock4/
    A clock application that prompts a signed-in user for a timezone
    offset to customize the display, and remembers the preference for
    future sessions using the datastore.

python/ch02/clock5/
    An improved version of the customizable clock that caches the
    user's preference data using the memcache, resulting in a faster
    user experience.

python/ch03/appcaching/
    A demonstration of how app caching works, in Python.

python/ch03/environment/
    Prints information about the Python environment, such as
    environment variables, the app server filesystem, and the request
    data.

python/ch03/googleaccounts/
    Configuring Google Accounts authentication, in Python.

python/ch03/logging/
    A simple demonstration of the Python logging module.

python/ch03/secureconnections/
    Configuring secure connections, in Python.

python/ch03/staticfiles/
    Configuring static files, in Python.

python/ch03/zipimport/
    Loading a Python module from a ZIP archive using zipimport.

python/ch03/zipserve/
    Serving files from a ZIP archive using zipserve.

python/ch04/bookexpando/
    Creating "Book" entities using an "expando" class.

python/ch04/bookmodel/
    Creating "Book" entities using a model class.

python/ch04/commentform/
    A comment form similar to Example 4-2.

python/ch04/entities/
    Manipulating datastore entities.

python/ch04/types/
    A demonstration of entity property types, including MVPs.

python/ch05/gql/
    Using GQL and the GqlQuery class to perform queries.

python/ch05/mvps/
    Queries and multi-valued properties.

python/ch05/queries/
    Using the Query class to perform queries.

python/ch06/keys/
    A demonstration of keys, paths, and ancestor queries.

python/ch06/transactions/
    Performing transactions using the Python datastore API.

python/ch07/models/
    Defining models, and declaring and using properties.

python/ch07/properties/
    A demonstration of the built-in property declarations.

python/ch07/relationships/
    Defining relationships with reference properties.

python/ch07/relationships1to1/
    A simple example of one-to-one relationships used to detach large data.

python/ch07/relationshipskeylist/
    Many-to-many relationships using the key list method.

python/ch07/relatinoshipslinkmodel/
    Many-to-many relationships using the link model method.

python/ch07/polymodel/
    Using the PolyModel base class for type hierarchies and polymorphic queries.

python/ch07/inheritance/
    Using class inheritance with data models.

python/ch07/customproperties/
    Writing your own property declaration classes.

python/ch09/memcache/
    A demonstration of the features of the memcache API.

python/ch10/async/
    Three ways to call the URL Fetch service asynchronously.

python/ch10/urlfetch/
    Using the urlfetch API to access the URL Fetch service (synchronously).

python/ch10/urllib2/
    Using the urllib2 library to access the URL Fetch service.

python/ch11/sendingmail/
    Sending email messages in Python.

python/ch11/receivingmail/
    Receiving email messages in Python.

python/ch11/xmpp/
    Sending and receiving XMPP (chat) messages in Python.

python/ch12/bulkloader/
    Loader and exporter code for the bulk loader tool, and an app
    configured for the remote API.

python/ch12/remoteapi/
    An app configured for the remote API and a script that accesses
    the app's datastore remotely.

python/ch13/cron/
    A simple example of scheduled task (cron) configuration.

python/ch13/deferred/
    An example of using the deferred Python module and task handler to
    create tasks that call Python functions.

python/ch13/tasks/
    A simple example showing how task queues are configured, and how
    tasks are created.

python/ch14/djangohelper/
    An example of using the Django App Engine Helper to create a
    Django applicaton.  Includes the data model, unit testing and
    forms examples.

python/ch14/djangonohelper/
    An example of using Django without a helper package.
