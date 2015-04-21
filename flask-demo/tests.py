import sys
sys.path.insert(0, '/Users/dan/google-cloud-sdk/platform/google_appengine')
sys.path.insert(0, '/Users/dan/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(0, './lib')

import unittest
from google.appengine.ext import testbed

import main
import models

class MyBlogTestCase(unittest.TestCase):
	def setUp(self):
		self.tb = testbed.Testbed()
		self.tb.activate()
		self.tb.init_datastore_v3_stub()
		self.tb.init_memcache_stub()
		self.tb.init_user_stub()

		main.app.config['TESTING'] = True
		self.app = main.app.test_client()

	def tearDown(self):
		self.tb.deactivate()

class TestEntry(MyBlogTestCase):
	def test_entry(self):
		m = models.Entry(
			title='Test',
			text='Test entry text')
		m.put()
		self.assertIsNotNone(m.last_updated_date)

class MyBlogInteractions(MyBlogTestCase):
	def test_no_entries(self):
		rv = self.app.get('/')
		assert 'No entries here so far' in rv.data

	def test_one_entry(self):
		e = models.Entry(title='Test', text='Test text')
		e.put()

		rv = self.app.get('/')
		assert 'No entries here so far' not in rv.data

	def test_add(self):
		rv = self.app.post('/add', data=dict(
			title='<Hello>',
			text='<strong>HTML</strong> allowed here'),
		follow_redirects=True)
		assert 'No entries here so far' not in rv.data
		assert '&lt;Hello&gt;' in rv.data
		assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
	unittest.main()
