import jinja2
import os
import webapp2
import zipfile
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()))

class UserUpload(db.Model):
    user = db.UserProperty()
    description = db.StringProperty()
    blob = blobstore.BlobReferenceProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        uploads = None
        if user:
            q = UserUpload.all()
            q.filter('user =', user)
            q.ancestor(db.Key.from_path('UserUploadGroup', user.email()))
            uploads = q.fetch(100)

        upload_url = blobstore.create_upload_url('/upload')

        template = template_env.get_template('home.html')
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'uploads': uploads,
            'upload_url': upload_url,
        }
        self.response.write(template.render(context))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        description = self.request.params['description']
        for blob_info in self.get_uploads('upload'):
            upload = UserUpload(
                parent=db.Key.from_path('UserUploadGroup', user.email()),
                user=user,
                description=description,
                blob=blob_info.key())
            upload.put()
        self.redirect('/')

def get_upload(key_str, user):
    user = users.get_current_user()
    upload = None
    if key_str:
        upload = db.get(key_str)

    if (not user or not upload or upload.user != user):
        return None
    return upload

class ViewHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        upload = get_upload(self.request.params.get('key'),
                            users.get_current_user())
        if not upload:
            self.error(404)
            return

        self.send_blob(upload.blob)

class ViewHexHandler(webapp2.RequestHandler):
    def get(self):
        upload = get_upload(self.request.params.get('key'),
                            users.get_current_user())
        if not upload:
            self.error(404)
            return

        try:
            start = int(self.request.params.get('start', 0))
            end = int(self.request.params.get('end', 1024))
        except ValueError, e:
            pass
        if end < start or end - start > blobstore.MAX_BLOB_FETCH_SIZE:
            start = 0
            end = 1024

        # Read a range of bytes from the beginning of the Blobstore
        # value and display them as hex.
        bytes = blobstore.fetch_data(upload.blob, start, end)
        end = min(end, len(bytes))
        lines = []
        bytes_per_line = 20
        line_pattern = '%06X: %-' + str(bytes_per_line * 3) + 's %s'
        for i in xrange(0, end - start, bytes_per_line):
            subrange_end = min((end - start - i), bytes_per_line)
            value_strs = []
            value_chrs = []
            for offset in xrange(0, subrange_end):
                value_strs.append('%02X ' % ord(bytes[i+offset]))
                if ord(bytes[i+offset]) >= 32 and ord(bytes[i+offset]) <= 126:
                    value_chrs.append(bytes[i+offset])
                else:
                    value_chrs.append('.')
            lines.append(line_pattern % (i,
                                         ''.join(value_strs),
                                         ''.join(value_chrs)))
        hex_txt = '\n'.join(lines)

        template = template_env.get_template('viewhex.html')
        context = {
            'upload': upload,
            'hex': hex_txt,
            'start': start,
            'end': end,
        }
        self.response.write(template.render(context))

class ViewZipHandler(webapp2.RequestHandler):
    def get(self):
        upload = get_upload(self.request.params.get('key'),
                            users.get_current_user())
        if not upload:
            self.error(404)
            return

        reader = blobstore.BlobReader(upload.blob)
        zip = zipfile.ZipFile(reader, 'r')
        info_list = zip.infolist()

        template = template_env.get_template('viewzip.html')
        context = {
            'upload': upload,
            'info_list': info_list,
        }
        self.response.write(template.render(context))

class DeleteHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            entities_to_delete = []
            blobs_to_delete = []
            for delete_key in self.request.params.getall('delete'):
                upload = db.get(delete_key)
                if upload.user != user:
                    continue
                entities_to_delete.append(upload.key())
                blobs_to_delete.append(upload.blob.key())

            db.delete(entities_to_delete)
            blobstore.delete(blobs_to_delete)

        self.redirect('/')

application = webapp2.WSGIApplication([('/', MainPage),
                                       ('/upload', UploadHandler),
                                       ('/viewhex', ViewHexHandler),
                                       ('/viewzip', ViewZipHandler),
                                       ('/view', ViewHandler),
                                       ('/delete', DeleteHandler)],
                                      debug=True)
