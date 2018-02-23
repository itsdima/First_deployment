from django.conf.urls import url 
from . import views 

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register), 
	url(r'^login$', views.login), 
	url(r'^books$', views.books),
	url(r'^logout$', views.logout),
	url(r'^users/(?P<number>\d+)$', views.viewUser), 
	url(r'^books/add$', views.addBook), 
	url(r'^books/(?P<number>\d+)$', views.viewBook),
	url(r'^book/process$', views.process),
	url(r'^quickreview/(?P<number>\d+)$', views.quickreview), 
	url(r'^destroy/(?P<number>\d+)$', views.destroy)
]