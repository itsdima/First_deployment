# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages


# Create your views here.

def index(request):
	return render(request, 'login_registration_app/index.html')

def register(request):
	result = User.objects.registrationValidate(request.POST)
	print result
	if result['status']:
		request.session['user_id'] = result['user'].id
	else: 
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/')
	return redirect('/books')

def login(request):
	result = User.objects.loginValidate(request.POST)
	if result['status'] == False:
		for error in result['errors']:
			messages.warning(request, error)
		return redirect('/')
	request.session['user_id'] = result['user'].id
	return redirect('/books')

def logout(request):
	request.session.clear()
	return redirect('/')

def books(request):
	if 'user_id' not in request.session:
		return redirect('/')
	tempid= request.session['user_id']
	ActiveUser = User.objects.get(id=tempid)
	allreviews = Review.objects.all().order_by('-created_at')
	otherbooks = Review.objects.all().order_by('created_at')
	morereviews = ''
	if len(allreviews) > 3:
		allreviews = [allreviews[0], allreviews[1], allreviews[2]]
	if len(otherbooks)> 3:
		temp = otherbooks.last()
		morereviews = otherbooks.exclude(id=allreviews[0].id).exclude(id=allreviews[1].id).exclude(id=allreviews[2].id)
	context = {
	'id': ActiveUser.id,
	'name': ActiveUser.name,
	'review': allreviews,
	'others': morereviews
	}
	return render(request, 'login_registration_app/success.html', context)

def viewUser(request, number):
	if 'user_id' not in request.session:
		return redirect('/')
	thisUser = User.objects.get(id=number)
	context = {
	'viewUser': thisUser,
	'count': thisUser.posted.count(), 
	'leftReview': thisUser.posted.all()
	}
	return render(request, 'login_registration_app/userinfo.html', context)

def viewBook(request, number):
	if 'user_id' not in request.session:
		return redirect('/')
	getbook = Book.objects.get(id=number)
	bookinfo = {
	'book': getbook.review.all(),
	'review': Review.objects.filter(book=getbook),
	'id': number,
	'thisbook': Book.objects.get(id=number),
	'userID': request.session['user_id']
	}
	return render(request, 'login_registration_app/displaybook.html', bookinfo)

def addBook(request):
	if 'user_id' not in request.session:
		return redirect('/')
	context = {
	'allauthors': Book.objects.raw('SELECT * FROM login_registration_app_book GROUP BY author')
	}
	return render(request, 'login_registration_app/addBook.html', context)

def process(request):
	title = request.POST['title']
	if len(request.POST['newauthor']) < 1:
		author = request.POST['author']
	else:
		author = request.POST['newauthor']
	uploader = request.session['user_id']
	thisUser = User.objects.get(id=uploader)
	Book.objects.create(title=title, author=author, posted_by=thisUser)
	book = Book.objects.last()
	Review.objects.create(rating=request.POST['newrating'], comment=request.POST['newreview'], posted_by=thisUser, book=book)
	return redirect('/books/'+ str(book.id))

def quickreview(request, number):
	thisUser = User.objects.get(id=request.session['user_id'])
	book = Book.objects.get(id=number)
	print request.POST['quickrating']
	Review.objects.create(rating=request.POST['quickrating'], comment=request.POST['quickreview'], posted_by=thisUser, book=book)
	return redirect('/books/'+ str(book.id))

def destroy(request, number):
	delete = Review.objects.get(id=number)
	bookID = delete.book.id
	delete.delete()
	return redirect('/books/'+str(bookID))