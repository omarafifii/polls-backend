from django.urls import path
from . import views

urlpatterns = [
	path('', views.getPolls, name="getPolls"),
	path('pollchoices/<int:pk>/', views.getPollChoices, name="getPollChoices"),
	path('search/<str:key>/', views.search, name="search"),
	path('vote/', views.vote, name="vote"),
	path('confirm/', views.confirm, name="confirm"),
	
]