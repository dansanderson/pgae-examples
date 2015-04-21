from google.appengine.ext import ndb

def is_non_empty_(prop, val):
    if len(val) > 0:
        return
    raise Exception('Property value is empty')

class Entry(ndb.Model):
    title = ndb.StringProperty(
        required=True,
        validator=is_non_empty_)
    text = ndb.TextProperty(required=True)
    last_updated_date = ndb.DateTimeProperty(auto_now=True)
