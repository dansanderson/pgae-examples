from google.appengine.ext import db
import datetime

print 'Content-Type: text/html'
print ''

def is_recent_year(val):
    if val < 1923:
        raise db.BadValueError

class MyModel(db.Model):
    # p1 must be a short string; default is None; not required
    p1 = db.StringProperty()

    # p2 must be a short string; cannot be None
    p2 = db.StringProperty(required=True)

    # p3 must be a short string; set to 'a default value' if not initialized
    p3 = db.StringProperty(default='a default value')

    # p4 must be 'Winter', 'Spring', 'Summer' or 'Autumn'; implies required=True
    p4 = db.StringProperty(choices=['Winter', 'Spring', 'Summer', 'Autumn'])

    # p5 will not appear in any indexes and cannot be used in queries
    p5 = db.StringProperty(indexed=False)

    # p6 must be a long integer >= 1923, as defined in the function is_recent_year
    p6 = db.IntegerProperty(validator=is_recent_year)

    string_prop = db.StringProperty()
    text_prop = db.TextProperty()
    bytestring_prop = db.ByteString()
    blob_prop = db.BlobProperty()
    boolean_prop = db.BooleanProperty()
    integer_prop = db.IntegerProperty()
    float_prop = db.FloatProperty()
    date_prop = db.DateProperty()
    datetime_prop = db.DateTimeProperty()
    time_prop = db.TimeProperty()
    user_prop = db.UserProperty()

    # auto_now_prop is automatically set to datetime.datetime.now()
    # every time the object is created or loaded from the datastore.
    auto_now_prop = db.DateTimeProperty(auto_now=True)

    # auto_now_add_prop is automatically set to
    # datetime.datetime.now() when the object is first created.  The
    # value is preserved for subsequent updates.
    auto_now_add_prop = db.DateTimeProperty(auto_now_add=True)

    # auto_current_user_prop is automatically set to
    # users.get_current_user() every time the object is created or
    # loaded from the datastore.  (This is None if the user is not
    # signed in to Google Accounts.)
    auto_current_user_prop = db.UserProperty(auto_current_user=True)

    # auto_current_user_add_prop is automatically set to
    # users.get_current_user() when the object is first created.  The
    # value is preserved for subsequent updates.
    auto_current_user_add_prop = db.UserProperty(auto_current_user_add=True)

    # integer_list_prop accepts a list of long integer values,
    # possibly an empty list.
    integer_list_prop = db.ListProperty(long)

    # string_list_prop accepts a list of string values, possibly an
    # empty list.
    string_list_prop = db.StringListProperty()


try:
    obj = MyModel()
except db.BadValueError, e:
    print '''<p>I cannot create a MyModel without initializing p2, which is
cannot be None, p4, which must be one of several string values, and p6, whose
value must meet a custom condition.</p>'''

try:
    obj = MyModel(p2='value', p4='Fall', p6=1978)
except db.BadValueError, e:
    print '''<p>I cannot create a MyModel with p4='Fall', since that is not
one of the valid choices declared for that property.</p>'''

try:
    obj = MyModel(p2='value', p4='Autumn', p6=1909)
except db.BadValueError, e:
    print '''<p>I cannot create a MyModel with p6=1909, since that is not a
valid value according to the custom validator function.</p>'''

obj = MyModel(p2='value', p4='Autumn', p6=1978)
print '''<p>I can create a MyModel with p2='value', p4='Autumn' and p6=1978,
since those values meet the required conditions of the property declarations
and all other property declarations allow their default values.</p>'''

print '<p>Property values of this object after initialization:</p><ul>'
prop_names = MyModel.properties().keys()
prop_names.sort()
for p in prop_names:
    print '<li>%s = %s</li>' % (p, repr(getattr(obj, p)))
print '</ul>'

print '<p>Assigning a non-empty list to integer_list_prop...</p>'
obj.integer_list_prop = [ 2, 4, 6, 8 ]

print '<p>Overriding automatic values for auto_now_add_prop and auto_now_prop...</p>'
obj.auto_now_add_prop = datetime.datetime(1999, 12, 31, 23, 59, 59, 0)
obj.auto_now_prop = datetime.datetime(1999, 12, 31, 23, 59, 59, 0)

print '<p>Saving...</p>'
obj.put()

print '<p>Property values of this object after saving:</p><ul>'
prop_names = MyModel.properties().keys()
prop_names.sort()
for p in prop_names:
    print '<li>%s = %s</li>' % (p, repr(getattr(obj, p)))
print '</ul>'

print '<p>Deleted the entity.</p>'
db.delete(obj)

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
