Running the Python Examples
---------------------------

The python/ directory contains examples for Google App Engine's Python
runtime environment.  In order to run a Python example on your
computer, you need Python 2.7 (not 3.x) and the Google App Engine
Python SDK.

You can download Python 2.7.x from the Python website:
  http://www.python.org/

You can download the App Engine Python SDK from here:
  http://developers.google.com/appengine/downloads

To run a Python example, use the "dev_appserver.py" command provided
by the SDK with the example's project directory as the first argument:
  dev_appserver.py python/clock/clock1

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
  appcfg.py update --application=APP-ID --version=VERSION-ID python/clock/clock1

The --application and --version arguments override the settings in the
example's app.yaml file.  The command prompts you for your Google
account email address and password, and uploads the example.

Test the uploaded example by visiting the corresponding appspot.com
URL:
  http://VERSION-ID.APP-ID.appspot.com/

* Note: When you upload an example that performs datastore queries,
  App Engine may need to build indexes requested by the application's
  configuration before it can serve requests for the example
  successfully.  If you get a NeedIndexError, check the Administration
  Console's "Datastore Indexes" to check the status of the index
  building process.


The Python Examples
-------------------

Chapter 2

python/clock/clock1/
    A simple Python app, with an app.yaml configuration file and a
    main.py request handler, using the webapp2 framework.  The request
    handler prints a dynamic message that appears in the browser.

python/clock/clock2/
    An example with Google Accounts sign-in and sign-out
    functionality.  This example also introduces Jinja2 templates for
    rendering HTML.

python/clock/clock3/
    A clock application that prompts a signed-in user for a timezone
    offset to customize the display, and remembers the preference for
    future sessions using the datastore.

python/clock/clock4/
    An improved version of the customizable clock that caches the
    user's preference data using the memcache, resulting in a faster
    user experience.


Chapter 3

python/configuration/appcaching/
    A demonstration of how app caching works, in Python.

python/configuration/environment/
    Prints information about the Python environment, such as
    environment variables, the app server filesystem, and the request
    data.

python/configuration/googleaccounts/
    Configuring Google Accounts authentication, in Python.

python/configuration/logging/
    A simple demonstration of the Python logging module.

python/configuration/secureconnections/
    Configuring secure connections, in Python.

python/configuration/staticfiles/
    Configuring static files, in Python.

python/configuration/zipimport/
    Loading a Python module from a ZIP archive using zipimport.

python/configuration/zipserve/
    Serving files from a ZIP archive using zipserve.


Chapter 5

python/datastore/allocateids/
    Allocating numeric IDs prior to creating entities.

python/datastore/bookexpando/
    Creating "Book" entities using an "expando" class.

python/datastore/bookmodel/
    Creating "Book" entities using a model class.

python/datastore/commentform/
    A comment form similar to Example 4-2.

python/datastore/entities/
    Manipulating datastore entities.

python/datastore/types/
    A demonstration of entity property types, including MVPs.


Chapter 6

python/datastore/cursors/
    A simple paginated display using query cursors.

python/datastore/gql/
    Using GQL and the GqlQuery class to perform queries.

python/datastore/mvps/
    Queries and multi-valued properties.

python/datastore/queries/
    Using the Query class to perform queries.


Chapter 7

python/datastore/keys/
    A demonstration of keys, paths, and ancestor queries.

python/datastore/transactions/
    Performing transactions using the Python datastore API.


Chapter 8

python/remoteapi/remoteapi/
    An app configured for the remote API and a script that accesses
    the app's datastore remotely.


Chapter 9

python/ext_db/models/
    Defining models, and declaring and using properties.

python/ext_db/properties/
    A demonstration of the built-in property declarations.

python/ext_db/relationships/
    Defining relationships with reference properties.

python/ext_db/relationships1to1/
    A simple example of one-to-one relationships used to detach large data.

python/ext_db/relationshipskeylist/
    Many-to-many relationships using the key list method.

python/ext_db/relatinoshipslinkmodel/
    Many-to-many relationships using the link model method.

python/ext_db/polymodel/
    Using the PolyModel base class for type hierarchies and polymorphic queries.

python/ext_db/inheritance/
    Using class inheritance with data models.

python/ext_db/customproperties/
    Writing your own property declaration classes.


Chapter 11

python/memcache/memcache/
    A demonstration of the features of the memcache API.


Chapter 12

python/blobstore/blobstore/
    A full demonstration app that accepts user uploads to the
    Blobstore, and allows the user to view and delete the values.


Chapter 13

python/urlfetch/async/
    Three ways to call the URL Fetch service asynchronously.

python/urlfetch/urlfetch/
    Using the urlfetch API to access the URL Fetch service (synchronously).

python/urlfetch/urllib2/
    Using the urllib2 library to access the URL Fetch service.


Chapter 14

python/mail/mail/
    Sending and receiving email messages in Python.


Chapter 15

python/xmpp/xmpp/
    A full demonstration app that can send and receive XMPP chat and
    presence messages, in Java.


Chapter 16

python/tasks/cron/
    A simple example of scheduled task (cron) configuration.

python/tasks/deferred/
    An example of using the deferred Python module and task handler to
    create tasks that call Python functions.

python/tasks/tasks/
    A simple example showing how task queues are configured, and how
    tasks are created.
