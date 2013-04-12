import sys
sys.path.insert(0, 'packages.zip')

import datetime
from bigpackage import bigmodule

print 'Content-Type: text/html'
print ''

bigmodule.print_message()

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
