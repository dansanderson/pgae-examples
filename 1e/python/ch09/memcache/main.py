import datetime
from google.appengine.api import memcache

print 'Content-Type: text/html'
print ''

headlines = ['...', '...', '...']

# Set or replace a memcache value.
success = memcache.set('headlines', headlines)
if not success:
    print '<p>Could not set "headlines".</p>'
else:
    print '<p>Set "headlines".</p>'

# Set a memcache value only if is not already set.
success = memcache.add('headlines', headlines)
if not success:
    print '<p>Could not add "headlines". (It\'s already set.)</p>'
else:
    print '<p>Added "headlines".</p>'

# Replace a memcache value only if it is already set.
success = memcache.replace('headlines', headlines)
if not success:
    print '<p>Could not replace "headlines".</p>'
else:
    print '<p>Replaced "headlines".'

# Get a memcache value.
headlines = memcache.get('headlines')
if headlines is None:
    print '<p>Could not get "headlines".</p>'
else:
    print '<p>Got "headlines": %s</p>' % repr(headlines)


# Batch calls.
article_summaries = {'article00174': '...',
                     'article05234': '...',
                     'article15820': '...',
                     }
failed_keys = memcache.set_multi(article_summaries)
if failed_keys:
    print '<p>set_multi failed for these keys: %s</p>' % ' '.join(failed_keys)
else:
    print '<p>set_multi succeeded.</p>'

article_summary_keys = ['article00174',
                        'article05234',
                        'article15820',
                        ]
article_summaries = memcache.get_multi(article_summary_keys)
print ('<p>Got article summaries using get_multi: %s</p>'
       % ' '.join(article_summaries.keys()))


# Batch calls with key prefixes.
article_summaries = {'00174': '...',
                     '05234': '...',
                     '15820': '...',
                     }
failed_keys = memcache.set_multi(article_summaries,
                                 key_prefix='article')
if failed_keys:
    print ('<p>set_multi with key prefix failed for these keys: %s</p>'
           % ' '.join(failed_keys))
else:
    print '<p>set_multi with key prefix succeeded.</p>'

article_summary_keys = ['00174',
                        '05234',
                        '15820',
                        ]
article_summaries = memcache.get_multi(article_summary_keys,
                                       key_prefix='article')
print ('<p>Got article summaries using get_multi with key prefix: %s</p>'
       % ' '.join(article_summaries.keys()))


# Namespaces.
article_summaries = {'article00174': '...',
                     'article05234': '...',
                     'article15820': '...',
                     }
failed_keys = memcache.set_multi(article_summaries,
                                 namespace='News')
if failed_keys:
    print ('<p>set_multi with key prefix failed for these keys: %s</p>'
           % ' '.join(failed_keys))
else:
    print '<p>set_multi with key prefix succeeded.</p>'

summary = memcache.get('article05234',
                       namespace='News')
if not summary:
    print '<p>Failed to get a value using a namespace.</p>'
else:
    print '<p>Got a value using a namespace.</p>'


# Cache expiration.
success = memcache.set('headlines', headlines,
                       time=300)
if not success:
    print '<p>Could not set "headlines" with an expiration.</p>'
else:
    print '<p>Set "headlines" with an expiration.</p>'


# Deleting keys.
result = memcache.delete('headlines')
if not result:
    print '<p>Could not delete "headlines".</p>'
else:
    print '<p>Deleted "headlines".</p>'

# Deleting with an add lock timer.
success = memcache.set('tempname91512', '...')
if not success:
    print '<p>Could not set "tempname91512".</p>'
else:
    result = memcache.delete('tempnode91512',
                             seconds=5)
    success = memcache.set('tempname91512', '...')
    if not success:
        print '<p>Could not set "tempname91512" during add-lock period.</p>'
    else:
        print ('<p>Set "tempname91512" during add-lock period. Note that the '
               'dev server doesn\'t support the add-lock.</p>')


# Incrementing a counter value.
work_done = memcache.incr('work_done', initial_value=0)
print '<p>Incremented "work_done": %d</p>' % work_done


# Cache statistics.
stats = memcache.get_stats()
print '<p>Memcache stats:</p><ul>'
for stat in stats.iteritems():
    print '<li>%s = %d' % stat
print '</ul>'


# Flush all keys.
memcache.flush_all()
print '<p>Flushed memcache.</p>'


print '<p>The time is: %s</p>' % str(datetime.datetime.now())
