from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^books/book/(\d*)', 'bookstore.views.book_form'),
    (r'^books/', 'bookstore.views.home'),
)
