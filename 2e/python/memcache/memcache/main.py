import datetime
import webapp2
from google.appengine.api import memcache

class MainPage(webapp2.RequestHandler):
    def get(self):

        headlines = ['...', '...', '...']
        
        # Set or replace a memcache value.
        success = memcache.set('headlines', headlines)
        if not success:
            self.response.write('<p>Could not set "headlines".</p>')
        else:
            self.response.write('<p>Set "headlines".</p>')
        
        # Set a memcache value only if is not already set.
        success = memcache.add('headlines', headlines)
        if not success:
            self.response.write('<p>Could not add "headlines". '
                                '(It\'s already set.)</p>')
        else:
            self.response.write('<p>Added "headlines".</p>')
        
        # Replace a memcache value only if it is already set.
        success = memcache.replace('headlines', headlines)
        if not success:
            self.response.write('<p>Could not replace "headlines".</p>')
        else:
            self.response.write('<p>Replaced "headlines".')
        
        # Get a memcache value.
        headlines = memcache.get('headlines')
        if headlines is None:
            self.response.write('<p>Could not get "headlines".</p>')
        else:
            self.response.write('<p>Got "headlines": %s</p>' % repr(headlines))
        
        
        # Batch calls.
        article_summaries = {'article00174': '...',
                             'article05234': '...',
                             'article15820': '...',
                             }
        failed_keys = memcache.set_multi(article_summaries)
        if failed_keys:
            self.response.write('<p>set_multi failed for these keys: %s</p>'
                                % ' '.join(failed_keys))
        else:
            self.response.write('<p>set_multi succeeded.</p>')
        
        article_summary_keys = ['article00174',
                                'article05234',
                                'article15820',
                                ]
        article_summaries = memcache.get_multi(article_summary_keys)
        self.response.write(('<p>Got article summaries using get_multi: %s</p>'
               % ' '.join(article_summaries.keys())))
        
        
        # Batch calls with key prefixes.
        article_summaries = {'00174': '...',
                             '05234': '...',
                             '15820': '...',
                             }
        failed_keys = memcache.set_multi(article_summaries,
                                         key_prefix='article')
        if failed_keys:
            self.response.write(('<p>set_multi with key prefix failed for these keys: %s</p>'
                   % ' '.join(failed_keys)))
        else:
            self.response.write('<p>set_multi with key prefix succeeded.</p>')
        
        article_summary_keys = ['00174',
                                '05234',
                                '15820',
                                ]
        article_summaries = memcache.get_multi(article_summary_keys,
                                               key_prefix='article')
        self.response.write(('<p>Got article summaries using get_multi with '
                             'key prefix: %s</p>'
                             % ' '.join(article_summaries.keys())))
        
        
        # Namespaces.
        article_summaries = {'article00174': '...',
                             'article05234': '...',
                             'article15820': '...',
                             }
        failed_keys = memcache.set_multi(article_summaries,
                                         namespace='News')
        if failed_keys:
            self.response.write(('<p>set_multi with key prefix failed for '
                                 'these keys: %s</p>'
                                 % ' '.join(failed_keys)))
        else:
            self.response.write('<p>set_multi with key prefix succeeded.</p>')
        
        summary = memcache.get('article05234',
                               namespace='News')
        if not summary:
            self.response.write('<p>Failed to get a value using a '
                                'namespace.</p>')
        else:
            self.response.write('<p>Got a value using a namespace.</p>')
        
        
        # Cache expiration.
        success = memcache.set('headlines', headlines,
                               time=300)
        if not success:
            self.response.write('<p>Could not set "headlines" with an '
                                'expiration.</p>')
        else:
            self.response.write('<p>Set "headlines" with an expiration.</p>')
        
        
        # Deleting keys.
        result = memcache.delete('headlines')
        if not result:
            self.response.write('<p>Could not delete "headlines".</p>')
        else:
            self.response.write('<p>Deleted "headlines".</p>')
        
        # Deleting with an add lock timer.
        success = memcache.set('tempname91512', '...')
        if not success:
            self.response.write('<p>Could not set "tempname91512".</p>')
        else:
            result = memcache.delete('tempnode91512',
                                     seconds=5)
            success = memcache.set('tempname91512', '...')
            if not success:
                self.response.write('<p>Could not set "tempname91512" '
                                    'during add-lock period.</p>')
            else:
                self.response.write(('<p>Set "tempname91512" during add-lock '
                                     'period. Note that the '
                                     'dev server doesn\'t support the '
                                     'add-lock.</p>'))
        
        
        # Incrementing a counter value.
        work_done = memcache.incr('work_done', initial_value=0)
        self.response.write('<p>Incremented "work_done": %d</p>' % work_done)
        
        
        # Cache statistics.
        stats = memcache.get_stats()
        self.response.write('<p>Memcache stats:</p><ul>')
        for stat in stats.iteritems():
            self.response.write('<li>%s = %d' % stat)
        self.response.write('</ul>')
        
        
        # Flush all keys.
        memcache.flush_all()
        self.response.write('<p>Flushed memcache.</p>')
        
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
