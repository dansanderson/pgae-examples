import datetime
import logging
import sys

print 'Content-Type: text/html'
print ''

logging.debug('debug level')
logging.info('info level')
logging.warning('warning level')
logging.error('error level')
logging.critical('critical level')

sys.stderr.write('stderr write, logged at the error level\n')

print '<p>Messages logged.</p>'
print '<p>The time is: %s</p>' % str(datetime.datetime.now())
