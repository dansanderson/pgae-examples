from django.shortcuts import render_to_response
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from django.http import HttpResponseRedirect
from bookstore import models

def home(request):
    q = models.Book.all().order('title')
    return render_to_response('bookstore/index.html',
                              { 'books': q })

class BookForm(djangoforms.ModelForm):
    class Meta:
        model = models.Book

def book_form(request, book_id=None):
    if request.method == 'POST':
        # The form was submitted.
        if book_id:
            # Fetch the existing Book and update it from the form.
            book = models.Book.get_by_id(int(book_id))
            form = BookForm(request.POST, instance=book)
        else:
            # Create a new Book based on the form.
            form = BookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)
            book.put()
            return HttpResponseRedirect('/books/')
        # else fail through to redisplay the form with error messages

    else:
        # The user wants to see the form.
        if book_id:
            # Show the form to edit an existing Book.
            book = models.Book.get_by_id(int(book_id))
            form = BookForm(instance=book)
        else:
            # Show the form to create a new Book.
            form = BookForm()

    return render_to_response('bookstore/bookform.html', {
        'book_id': book_id,
        'form': form,
    })
