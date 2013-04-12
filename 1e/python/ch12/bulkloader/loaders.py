from google.appengine.tools import bulkloader
import datetime

# Import the app's data models directly into
# this namespace.  We must add the app
# directory to the path explicitly.
import sys
import os.path
sys.path.append(
    os.path.abspath(
    os.path.dirname(
    os.path.realpath(__file__))))
from models import *

def get_date_from_str(s):
    if s:
        return datetime.datetime.strptime(s, '%m/%d/%Y').date()
    else:
        return None

class BookLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Book',
            [('title', str),
             ('author', str),
             ('copyright_year', int),
             ('author_birthdate', get_date_from_str),
             ])

loaders = [BookLoader]
