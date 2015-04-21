import flask
import os

from google.appengine.api import users

import models

app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

app.secret_key = '12345'

@app.route('/')
def show_entries():
    entries = models.Entry.query().order(-models.Entry.last_updated_date)
    return flask.render_template(
        'show_entries.html',
        entries=entries,
        user=users.get_current_user(),
        signin_url=users.create_login_url('/'),
        signout_url=users.create_logout_url('/'))

@app.route('/add', methods=['POST'])
def add_entry():
    entry = models.Entry(
        title=flask.request.form['title'],
        text=flask.request.form['text'])
    entry.put()
    flask.flash('New entry was successfully posted')
    return flask.redirect(flask.url_for('show_entries'))

@app.errorhandler(404)
def page_not_found(e):
    return 'Not found.', 404
