from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    form = request.POST
    errors = User.objects.reg_validator(form)
    if len(errors) > 0:
        for single_error in errors.values():
            messages.error(request, single_error)
        return redirect('/')
    hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
    current_user = User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=hashed_pw)
    request.session['user_id'] = current_user.id
    return redirect('/books')

def login(request):
    form=request.POST
    errors = User.objects.login_validator(form)
    if len(errors)>0:
        for single_error in errors.values():
            messages.error(request, single_error)
        return redirect('/')
    current_user = User.objects.get(email=form['email'])
    request.session['user_id'] = current_user.id
    return redirect('/books')

def books(request):
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'books':Book.objects.all(),
    }
    return render(request, 'books.html', context)

def add_book(request):
    form = request.POST
    # add validations for a new book
    current_user = User.objects.get(id=request.session['user_id'])
    new_book = Book.objects.create(title=form['title'], desc=form['desc'],uploaded_by=current_user)
    return redirect('/books')

def add_to_fav(request, book_id):
    current_user = User.objects.get(id=request.session['user_id'])
    current_book = Book.objects.get(id=book_id)
    current_user.liked_books.add(current_book)
    return redirect('/books')

def book_info(request, book_id):
    context={
        'book': Book.objects.get(id=book_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'book_info.html', context)

def unfav(request, book_id):
    current_book= Book.objects.get(id=book_id)
    current_user = User.objects.get(id=request.session['user_id'])
    current_book.users_who_like.remove(current_user)
    return redirect(f'/books/{book_id}')


def logout(request):
    request.session.clear()
    return redirect('/')

