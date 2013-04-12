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

def make_str_for_date(d):
    if d:
        return d.strftime('%m/%d/%Y')
    else:
        return ''

class BookExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Book',
            [('title', str, None),
             ('author', str, ''),
             ('copyright_year', int, ''),
             ('author_birthdate', make_str_for_date, ''),
             ])

exporters = [BookExporter]
